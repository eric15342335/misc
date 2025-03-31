WITH FilteredTexts AS (
  -- First, select distinct source texts with their minimum ID
  SELECT DISTINCT SourceText, MIN(Id) as MinId
  FROM TranslationHistory
  GROUP BY SourceText
),
NonContainedTexts AS (
  -- Then filter out texts that are contained within others
  SELECT FT1.SourceText, FT1.MinId
  FROM FilteredTexts FT1
  WHERE NOT EXISTS (
    SELECT 1 
    FROM FilteredTexts FT2
    WHERE FT2.SourceText != FT1.SourceText
    AND FT2.SourceText LIKE '%' || FT1.SourceText || '%'
  )
)

-- Finally, concatenate the filtered texts in ID order
select group_concat(SourceText) from (SELECT SourceText
FROM NonContainedTexts
ORDER BY MinId ASC) as a