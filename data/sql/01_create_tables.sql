-- BigQuery SQL schema creation script for ClaimGuard AI

CREATE SCHEMA IF NOT EXISTS `claimguard_demo`
OPTIONS(
  location="us-central1"
);

-- Claims Table
CREATE TABLE IF NOT EXISTS `claimguard_demo.claims` (
  claim_id STRING NOT NULL,
  customer_id STRING NOT NULL,
  vehicle_id STRING NOT NULL,
  incident_date DATE NOT NULL,
  claimed_amount NUMERIC NOT NULL,
  currency STRING NOT NULL,
  status STRING NOT NULL,
  risk_score INT64,
  created_at TIMESTAMP NOT NULL
);

-- Customers Table
CREATE TABLE IF NOT EXISTS `claimguard_demo.customers` (
  customer_id STRING NOT NULL,
  full_name STRING NOT NULL,
  policy_number STRING NOT NULL,
  total_historical_claims INT64 NOT NULL,
  prior_claims_under_review INT64 NOT NULL,
  customer_since DATE NOT NULL
);

-- Repair Estimates Baseline Table
CREATE TABLE IF NOT EXISTS `claimguard_demo.repair_estimates` (
  vehicle_category STRING NOT NULL,
  damage_type STRING NOT NULL,
  baseline_cost NUMERIC NOT NULL,
  currency STRING NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- Seed Baseline Data
INSERT INTO `claimguard_demo.repair_estimates` (vehicle_category, damage_type, baseline_cost, currency, updated_at)
VALUES
  ('Sedan - Midsize', 'Front bumper, headlight, bonnet', 210000, 'INR', CURRENT_TIMESTAMP()),
  ('Hatchback - Compact', 'Rear bumper scratch', 22000, 'INR', CURRENT_TIMESTAMP()),
  ('Hatchback - Midsize', 'Side door dent and suspension damage', 120000, 'INR', CURRENT_TIMESTAMP());
