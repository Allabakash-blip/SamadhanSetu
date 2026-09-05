-- Optional sample data for Milestone 8.
-- Run only after creating/approving an INDUSTRY user and confirming the IDs in your database.
-- Replace 10 with the real industry user ID and 3 with a real problem ID.

INSERT INTO industry_support_offers
(problem_id, industry_id, support_type, title, description, amount, duration, status, created_at, updated_at)
VALUES
(3, 10, 'PROTOTYPING', 'Prototype and field testing support',
 'Provide prototype components, technical mentoring and field testing support for the proposed village solution.',
 '₹2,50,000', '3 months', 'PROPOSED', NOW(), NOW());
