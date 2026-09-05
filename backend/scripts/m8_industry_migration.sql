-- Milestone 8: Industry Partnership Module
-- The FastAPI startup also creates these tables automatically.
-- Use this script only if you want to create them explicitly in Aiven/MySQL.

CREATE TABLE IF NOT EXISTS industry_support_offers (
  id INT NOT NULL AUTO_INCREMENT,
  problem_id INT NOT NULL,
  industry_id INT NOT NULL,
  support_type ENUM('MENTORING','FUNDING','TECHNICAL','PROTOTYPING','TESTING','TECHNOLOGY_TRANSFER','CSR','OTHER') NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  amount VARCHAR(100) NULL,
  duration VARCHAR(100) NULL,
  status ENUM('PROPOSED','ACCEPTED','REJECTED','WITHDRAWN') NOT NULL DEFAULT 'PROPOSED',
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY ix_industry_support_offers_problem_id (problem_id),
  KEY ix_industry_support_offers_industry_id (industry_id),
  KEY ix_industry_support_offers_support_type (support_type),
  KEY ix_industry_support_offers_status (status),
  CONSTRAINT fk_industry_offer_problem FOREIGN KEY (problem_id) REFERENCES problems(id),
  CONSTRAINT fk_industry_offer_user FOREIGN KEY (industry_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS industry_partnerships (
  id INT NOT NULL AUTO_INCREMENT,
  problem_id INT NOT NULL,
  industry_id INT NOT NULL,
  offer_id INT NULL,
  support_type ENUM('MENTORING','FUNDING','TECHNICAL','PROTOTYPING','TESTING','TECHNOLOGY_TRANSFER','CSR','OTHER') NOT NULL,
  scope TEXT NOT NULL,
  status ENUM('ACTIVE','COMPLETED','TERMINATED') NOT NULL DEFAULT 'ACTIVE',
  started_at DATETIME NOT NULL,
  completed_at DATETIME NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY ix_industry_partnerships_problem_id (problem_id),
  KEY ix_industry_partnerships_industry_id (industry_id),
  KEY ix_industry_partnerships_offer_id (offer_id),
  KEY ix_industry_partnerships_status (status),
  CONSTRAINT fk_industry_partnership_problem FOREIGN KEY (problem_id) REFERENCES problems(id),
  CONSTRAINT fk_industry_partnership_user FOREIGN KEY (industry_id) REFERENCES users(id),
  CONSTRAINT fk_industry_partnership_offer FOREIGN KEY (offer_id) REFERENCES industry_support_offers(id)
) ENGINE=InnoDB;
