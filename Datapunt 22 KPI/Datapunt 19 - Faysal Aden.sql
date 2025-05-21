USE hr;

DROP USER IF EXISTS 'kpidashboard'@'%';
CREATE USER 'kpidashboard'@'%' IDENTIFIED BY 'VeiligWachtwoord123';

CREATE OR REPLACE VIEW view_klanttevredenheid_jonge_klanten AS
SELECT 
    m.medewerker_id,
    m.voornaam,
    m.achternaam,
    m.geslacht,
    f.functienaam,
    COALESCE(oa.norm, a.default_norm) AS norm_klanttevredenheid,
    a.omschrijving AS omschrijving_afspraak
FROM 
    medewerker m
INNER JOIN 
    functie f ON m.functie_id = f.functie_id
LEFT JOIN 
    ontwikkelafspraak oa ON m.medewerker_id = oa.medewerker_id AND oa.afspraak_id = 1
INNER JOIN 
    afspraak a ON a.afspraak_id = 1
WHERE 
    m.functie_id = 1; 

GRANT SELECT ON view_klanttevredenheid_jonge_klanten TO 'kpidashboard'@'%';

FLUSH PRIVILEGES;

