

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE,
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    ProfilePicture VARCHAR(255)
);

CREATE TABLE Images (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ImagePath VARCHAR(255),
    UploadDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Votes (
    VoteID INT AUTO_INCREMENT PRIMARY KEY,
    ImageID INT,
    UserID INT,
    Type ENUM('like', 'dislike'),
    FOREIGN KEY (ImageID) REFERENCES Images(ImageID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Comments (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    ImageID INT,
    UserID INT,
    Text TEXT,
    CommentDate DATETIME,
    FOREIGN KEY (ImageID) REFERENCES Images(ImageID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Follows (
    FollowID INT AUTO_INCREMENT PRIMARY KEY,
    FollowerID INT,
    FolloweeID INT,
    FOREIGN KEY (FollowerID) REFERENCES Users(UserID),
    FOREIGN KEY (FolloweeID) REFERENCES Users(UserID)
);
