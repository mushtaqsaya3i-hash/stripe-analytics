# Stripe Payment Analytics Dashboard

A portfolio-ready analytics project that uses the Stripe API, Python, SQL, and Power BI to build an end-to-end payment analytics pipeline and business dashboard.

## Project Overview

This project demonstrates how payment transaction data can be collected from Stripe, transformed into an analytics-ready dataset, analyzed using SQL and Python, and presented through an interactive Power BI dashboard.

The project focuses on separating **business transactions** from **sandbox/test activity** and measuring payment performance, revenue, transaction volume, and payment status.

## Business Problem

Payment teams need visibility into:

- Total payment activity
- Successful payment revenue
- Payment success rate
- Average successful transaction value
- Revenue by business transaction type
- Successful vs unsuccessful payment value
- Business activity vs test/sandbox activity

This project creates a simple analytics workflow to answer these questions from Stripe payment data.

## Technology Stack

- **Stripe API** — payment transaction source
- **Python** — API integration and data extraction
- **Pandas / CSV** — data handling and export
- **SQLite** — analytical data storage
- **SQL** — transaction and revenue analysis
- **Power BI** — dashboard and visualization
- **Git / GitHub** — version control and portfolio delivery

## Architecture

```text
Stripe API
    ↓
Python Data Extraction
    ↓
CSV Dataset
    ↓
SQLite Database
    ↓
SQL Analysis / Business Views
    ↓
Power BI Dashboard
