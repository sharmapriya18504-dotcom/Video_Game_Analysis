-- Top 10 games
SELECT Name, Global_Sales
FROM vgsales
ORDER BY Global_Sales DESC
LIMIT 10;

-- Platform sales
SELECT Platform, SUM(Global_Sales) AS Total_Sales
FROM vgsales
GROUP BY Platform
ORDER BY Total_Sales DESC;

-- Genre sales
SELECT Genre, SUM(Global_Sales) AS Sales
FROM vgsales
GROUP BY Genre
ORDER BY Sales DESC;