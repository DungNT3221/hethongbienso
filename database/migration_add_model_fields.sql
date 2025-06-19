-- Migration: Add model_path and model_saved fields to train_jobs table
-- Date: 2025-06-08
-- Purpose: Support manual model saving workflow

USE trainregion_db;

-- Add new columns to train_jobs table
ALTER TABLE train_jobs 
ADD COLUMN model_path VARCHAR(500) DEFAULT NULL,
ADD COLUMN model_saved BOOLEAN DEFAULT FALSE;

-- Update existing completed jobs to have model_saved = FALSE
UPDATE train_jobs 
SET model_saved = FALSE 
WHERE status = 'completed';

-- Show updated table structure
DESCRIBE train_jobs;
