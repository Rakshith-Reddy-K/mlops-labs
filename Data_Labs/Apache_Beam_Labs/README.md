# Apache Beam E-commerce Analysis

This project demonstrates Apache Beam data processing with e-commerce transaction data.

## Project Structure

```
.
├── Try_Apache_Beam_Ecommerce.ipynb  # Main Jupyter notebook
├── data/
│   └── transactions.json            # Input transaction data (JSON Lines format)
├── outputs/
│   ├── category_sales-00000-of-00001      # Sales by category
│   ├── customer_spending-00000-of-00001   # Spending by customer
│   ├── high_value_orders-00000-of-00001   # Orders >= $500
│   └── product_stats-00000-of-00001       # Product statistics
└── README.md
```

## Input Data

The `transactions.json` file contains e-commerce transactions in JSON Lines format (one JSON object per line):

```json
{
  "order_id": "001",
  "customer": "Alice",
  "product": "Laptop",
  "category": "Electronics",
  "amount": 1200,
  "quantity": 1,
  "date": "2024-01-15"
}
```

**Fields:**

- `order_id`: Unique order identifier
- `customer`: Customer name
- `product`: Product name
- `category`: Product category (Electronics, Furniture, etc.)
- `amount`: Unit price
- `quantity`: Number of units ordered
- `date`: Order date

## Analyses Performed

The pipeline performs four parallel analyses:

### 1. Sales by Category

Aggregates total sales for each product category.

**Output:** `outputs/category_sales-*`

```
Category: Electronics, Total Sales: $3430.00
Category: Furniture, Total Sales: $1385.00
```

### 2. Customer Spending

Calculates total spending for each customer.

**Output:** `outputs/customer_spending-*`

```
Customer: Alice, Total Spent: $1630.00
Customer: Bob, Total Spent: $350.00
```

### 3. High-Value Orders

Identifies orders with total value >= $500.

**Output:** `outputs/high_value_orders-*`

```
Order 001: Alice - Laptop ($1200.00)
Order 004: Charlie - Chair ($600.00)
```

### 4. Product Statistics

Shows units sold and revenue for each product.

**Output:** `outputs/product_stats-*`

```
Product: Laptop, Units: 1, Revenue: $1200.00
Product: Mouse, Units: 2, Revenue: $50.00
```

## Running the Pipeline

### Prerequisites

```bash
pip install apache-beam
```

### Execute in Jupyter Notebook

1. Open `Try_Apache_Beam_Ecommerce.ipynb`
2. Run all cells sequentially
3. Check the `outputs/` directory for results

### Run as Python Script

Extract the pipeline code from the notebook and run:

```bash
python beam_ecommerce_analysis.py
```

## Key Concepts Demonstrated

1. **Custom DoFn Classes**: `ParseAndCalculate` and `FilterHighValue`
2. **Parallel Processing**: Multiple analyses on the same data stream
3. **Aggregations**: `CombinePerKey` for summing values
4. **Data Transformations**: Map, FlatMap, ParDo
5. **JSON Processing**: Parsing and working with structured data

## Data Summary

- **Total Orders**: 10
- **Total Revenue**: $4,815.00
- **Customers**: 5 (Alice, Bob, Charlie, David, Eve)
- **Products**: 10 unique products
- **Categories**: 2 (Electronics, Furniture)
- **High-Value Orders**: 4 orders >= $500

## Extending the Analysis

You can easily add more analyses:

- Average order value per customer
- Daily sales trends
- Category-wise product performance
- Customer segmentation by spending
- Product recommendations based on purchase patterns

## Apache Beam Features Used

- **PTransforms**: Map, FlatMap, ParDo, CombinePerKey
- **DoFn**: Custom data processing functions
- **I/O**: ReadFromText, WriteToText
- **Pipeline**: DirectRunner for local execution
