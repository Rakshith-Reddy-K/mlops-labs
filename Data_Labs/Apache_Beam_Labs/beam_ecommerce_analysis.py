#!/usr/bin/env python3
"""
Apache Beam E-commerce Transaction Analysis
Analyzes e-commerce data to provide insights on sales, customers, and products.
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import argparse


class ParseAndCalculate(beam.DoFn):
    """Parse JSON transaction and calculate total amount"""
    
    def process(self, element):
        """
        Args:
            element: JSON string representing a transaction
        
        Yields:
            dict: Transaction with calculated 'total' field
        """
        transaction = json.loads(element)
        transaction['total'] = transaction['amount'] * transaction['quantity']
        yield transaction


class FilterHighValue(beam.DoFn):
    """Filter transactions above a threshold value"""
    
    def __init__(self, threshold):
        """
        Args:
            threshold: Minimum transaction total to include
        """
        self.threshold = threshold
    
    def process(self, element):
        """
        Args:
            element: Transaction dictionary
        
        Yields:
            dict: Transaction if total >= threshold
        """
        if element['total'] >= self.threshold:
            yield element


class CombineProductStats(beam.CombineFn):
    """Properly combine product statistics across transactions"""
    
    def create_accumulator(self):
        """Create initial accumulator"""
        return {'units_sold': 0, 'total_revenue': 0.0, 'orders': 0}
    
    def add_input(self, accumulator, element):
        """Add a single element to the accumulator"""
        accumulator['units_sold'] += element['quantity']
        accumulator['total_revenue'] += element['revenue']
        accumulator['orders'] += 1
        return accumulator
    
    def merge_accumulators(self, accumulators):
        """Merge multiple accumulators"""
        merged = self.create_accumulator()
        for acc in accumulators:
            merged['units_sold'] += acc['units_sold']
            merged['total_revenue'] += acc['total_revenue']
            merged['orders'] += acc['orders']
        return merged
    
    def extract_output(self, accumulator):
        """Extract final output from accumulator"""
        return accumulator


def run_analysis(input_file, output_dir, high_value_threshold=500):
    """
    Execute the e-commerce analysis pipeline
    
    Args:
        input_file: Path to input transactions file (JSON Lines)
        output_dir: Directory for output files
        high_value_threshold: Minimum value for high-value order filter
    """
    
    # Define output paths
    category_output = f'{output_dir}/category_sales'
    customer_output = f'{output_dir}/customer_spending'
    highvalue_output = f'{output_dir}/high_value_orders'
    product_output = f'{output_dir}/product_stats'
    
    with beam.Pipeline(options=PipelineOptions()) as pipeline:
        
        # Read and parse transactions
        transactions = (
            pipeline
            | 'Read Transactions' >> beam.io.ReadFromText(input_file)
            | 'Parse and Calculate Total' >> beam.ParDo(ParseAndCalculate())
        )
        
        # Analysis 1: Total sales by category
        _ = (
            transactions
            | 'Extract Category-Amount' >> beam.Map(
                lambda t: (t['category'], t['total'])
            )
            | 'Sum by Category' >> beam.CombinePerKey(sum)
            | 'Format Category Results' >> beam.Map(
                lambda kv: f"Category: {kv[0]}, Total Sales: ${kv[1]:.2f}"
            )
            | 'Write Category Sales' >> beam.io.WriteToText(category_output)
        )
        
        # Analysis 2: Total spending by customer
        _ = (
            transactions
            | 'Extract Customer-Amount' >> beam.Map(
                lambda t: (t['customer'], t['total'])
            )
            | 'Sum by Customer' >> beam.CombinePerKey(sum)
            | 'Format Customer Results' >> beam.Map(
                lambda kv: f"Customer: {kv[0]}, Total Spent: ${kv[1]:.2f}"
            )
            | 'Write Customer Spending' >> beam.io.WriteToText(customer_output)
        )
        
        # Analysis 3: High-value orders
        _ = (
            transactions
            | 'Filter High Value Orders' >> beam.ParDo(
                FilterHighValue(high_value_threshold)
            )
            | 'Format High Value Orders' >> beam.Map(
                lambda t: (
                    f"Order {t['order_id']}: {t['customer']} - "
                    f"{t['product']} (${t['total']:.2f})"
                )
            )
            | 'Write High Value Orders' >> beam.io.WriteToText(highvalue_output)
        )
        
        # Analysis 4: Product statistics (FIXED VERSION)
        _ = (
            transactions
            | 'Extract Product Info' >> beam.Map(
                lambda t: (
                    t['product'],
                    {'quantity': t['quantity'], 'revenue': t['total']}
                )
            )
            | 'Aggregate Product Stats' >> beam.CombinePerKey(
                CombineProductStats()
            )
            | 'Format Product Stats' >> beam.Map(
                lambda kv: (
                    f"Product: {kv[0]}, "
                    f"Units: {kv[1]['units_sold']}, "
                    f"Revenue: ${kv[1]['total_revenue']:.2f}, "
                    f"Orders: {kv[1]['orders']}"
                )
            )
            | 'Write Product Stats' >> beam.io.WriteToText(product_output)
        )
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nResults written to: {output_dir}/")
    print(f"  - {category_output}-*")
    print(f"  - {customer_output}-*")
    print(f"  - {highvalue_output}-*")
    print(f"  - {product_output}-*")
    print("\n")


def main():
    """Parse arguments and run the analysis"""
    
    parser = argparse.ArgumentParser(
        description='Analyze e-commerce transactions with Apache Beam'
    )
    parser.add_argument(
        '--input',
        default='data/transactions.jsonl',
        help='Input file path (JSON Lines format)'
    )
    parser.add_argument(
        '--output',
        default='outputs',
        help='Output directory for results'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=500.0,
        help='Minimum value for high-value order filter (default: 500)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("E-COMMERCE TRANSACTION ANALYSIS")
    print("=" * 70)
    print(f"\nInput file: {args.input}")
    print(f"Output directory: {args.output}")
    print(f"High-value threshold: ${args.threshold:.2f}")
    print("\nStarting pipeline...\n")
    
    run_analysis(args.input, args.output, args.threshold)


if __name__ == '__main__':
    main()