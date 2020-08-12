SELECT DISTINCT(name) FROM people
JOIN movies ON stars.movie_id = movies.id
JOIN stars ON people.id = stars.person_id
WHERE movies.title IN (SELECT movies.title
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE people.birth=1958 AND people.name="Kevin Bacon") AND people.name!="Kevin Bacon";