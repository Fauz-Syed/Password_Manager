-- Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    HashedPassword VARCHAR(1000) NOT NULL,
    Salt VARCHAR(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Password Entries Table
CREATE TABLE PasswordEntries (
    EntryID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Website VARCHAR(255) NOT NULL,
    Web_Username VARCHAR(255),
    EncryptedPassword TEXT NOT NULL,
    Note TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Optional: Encryption Keys Table
CREATE TABLE EncryptionKeys (
    KeyID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    EncryptionKey VARBINARY(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Optional: Password History Table
CREATE TABLE PasswordHistory (
    HistoryID INT PRIMARY KEY AUTO_INCREMENT,
    EntryID INT,
    EncryptedPassword TEXT NOT NULL,
    ChangedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EntryID) REFERENCES PasswordEntries(EntryID) ON DELETE CASCADE
);

-- Optional: User Settings Table
CREATE TABLE UserSettings (
    SettingID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    SettingName VARCHAR(255) NOT NULL,
    SettingValue TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Optional: Audit Logs Table
CREATE TABLE AuditLogs (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Action VARCHAR(255) NOT NULL,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
-- Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    HashedPassword VARCHAR(255) NOT NULL,
    Salt VARCHAR(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Password Entries Table
CREATE TABLE PasswordEntries (
    EntryID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Website VARCHAR(255) NOT NULL,
    Username VARCHAR(255),
    EncryptedPassword TEXT NOT NULL,
    Note TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Optional: Encryption Keys Table
CREATE TABLE EncryptionKeys (
    KeyID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    EncryptionKey VARBINARY(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Optional: Password History Table
CREATE TABLE PasswordHistory (
    HistoryID INT PRIMARY KEY AUTO_INCREMENT,
    EntryID INT,
    EncryptedPassword TEXT NOT NULL,
    ChangedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EntryID) REFERENCES PasswordEntries(EntryID) ON DELETE CASCADE
);

-- Optional: User Settings Table
CREATE TABLE UserSettings (
    SettingID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    SettingName VARCHAR(255) NOT NULL,
    SettingValue TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Optional: Audit Logs Table
CREATE TABLE AuditLogs (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Action VARCHAR(255) NOT NULL,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
