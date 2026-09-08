WITH tb_cand AS (
    SELECT 
        SQ_CANDIDATO,
        SG_UF,
        DS_CARGO,
        NR_PARTIDO,
        SG_PARTIDO,
        NM_PARTIDO,
        DT_NASCIMENTO,
        DS_GENERO,
        DS_GRAU_INSTRUCAO,
        DS_ESTADO_CIVIL,
        DS_COR_RACA,
        DS_OCUPACAO
    FROM tse.bronze.consulta_cand
),
tb_partido_tratado AS (
    SELECT
        NR_PARTIDO,
        SG_PARTIDO,
        NM_PARTIDO
    FROM (
        SELECT
            NR_PARTIDO,
            SG_PARTIDO,
            NM_PARTIDO,
            ROW_NUMBER() OVER (
                PARTITION BY NR_PARTIDO ORDER BY count(*) DESC
            ) AS ordem
        FROM tse.bronze.consulta_cand
        GROUP BY NR_PARTIDO, SG_PARTIDO, NM_PARTIDO
    ) AS tb_grafias
    WHERE ordem = 1
),
tb_total_bens AS (
    SELECT
        SQ_CANDIDATO,
        sum(cast(replace(VR_BEM_CANDIDATO, ',', '.') as DECIMAL(15,2))) AS total_bens
        FROM tse.bronze.bem_candidato
        GROUP BY 1
),
tb_info_completa_cand AS (
    SELECT
        t1.*,
        COALESCE(t2.total_bens, 0) AS totalBens,
        CAST(
            datediff(
                DATE('2024-10-06'),
                to_date(DT_NASCIMENTO, 'dd/MM/yyyy')
            ) / 365.25
        AS INT) AS NR_IDADE
    FROM tb_cand AS t1
    LEFT JOIN tb_total_bens AS t2
    ON t1.SQ_CANDIDATO = t2.SQ_CANDIDATO
)

SELECT
    p.SG_PARTIDO,
    t1.DS_CARGO,
    SG_UF,
    AVG(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS txGeneroFeminino,
    SUM(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS totalGeneroFeminino,
    AVG(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS txCorRacaPreta,
    SUM(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS totalCorRacaPreta,
    AVG(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS txCorRacaNaoBranca,
    SUM(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS totalCorRacaNaoBranca,
    SUM(t1.totalBens) AS totalBens,
    AVG(t1.totalBens) AS avgBens,
    COALESCE(AVG(CASE WHEN totalBens > 1 THEN totalBens END), 0) AS avgBensNotZero,
    SUM(CASE WHEN totalBens > 1 THEN totalBens ELSE 0 END) AS totalBensNotZero,
    SUM(CASE WHEN totalBens > 1 THEN 1 ELSE 0 END) AS totalCandidatosNotZero,
    AVG(t1.NR_IDADE) AS avgIdade,
    SUM(t1.NR_IDADE) AS totalIdade,
    count(*) AS totalCandidatos
FROM tb_info_completa_cand AS t1
LEFT JOIN tb_partido_tratado AS p
ON t1.NR_PARTIDO = p.NR_PARTIDO
GROUP BY p.SG_PARTIDO, t1.DS_CARGO, SG_UF WITH CUBE
ORDER BY p.SG_PARTIDO, t1.DS_CARGO, SG_UF