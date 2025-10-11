-- 创建数据库（如果还没有）
CREATE DATABASE IF NOT EXISTS ai_llm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE ai_llm;

-- 创建 subject 表
CREATE TABLE subject (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 chatcontent 表
CREATE TABLE chatcontent (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subjectid INT NOT NULL,
    content TEXT NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subjectid) REFERENCES subject(id) ON DELETE CASCADE,
    INDEX idx_subjectid (subjectid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;