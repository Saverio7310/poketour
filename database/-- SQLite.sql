-- SQLite con shift option a si commenta a più linee
-- SELECT name, count(*) FROM teams_OCpGIIa9m9BGzlZ8B5Gt where name = 'Arcanine' and movea = 'Flare Blitz' and moveb = 'Protect' and movec = 'Extreme Speed' and moved = 'Will-O-Wisp'
/* SELECT movea, moveb, movec, moved, count(*) FROM teams_OCpGIIa9m9BGzlZ8B5Gt 
WHERE 
name = 'Arcanine' AND
movea in ('Flare Blitz', 'Protect', 'Extreme Speed', 'Will-O-Wisp') AND
moveb in ('Flare Blitz', 'Protect', 'Extreme Speed', 'Will-O-Wisp') AND
movec in ('Flare Blitz', 'Protect', 'Extreme Speed', 'Will-O-Wisp') AND
moved in ('Flare Blitz', 'Protect', 'Extreme Speed', 'Will-O-Wisp')
GROUP BY movea, moveb, movec, moved
ORDER BY movea, moveb, movec, moved */

SELECT name, ability FROM teams_OCpGIIa9m9BGzlZ8B5Gt WHERE name = 'Dondozo' 