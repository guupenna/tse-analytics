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
    FROM tb_candidaturas
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
        FROM tb_candidaturas
        GROUP BY NR_PARTIDO, SG_PARTIDO, NM_PARTIDO
    ) AS tb_grafias
    WHERE ordem = 1
),
tb_total_bens AS (
    SELECT
        SQ_CANDIDATO,
        sum(cast(replace(VR_BEM_CANDIDATO, ',', '.') as DECIMAL(15,2))) AS total_bens
        FROM tb_bens
        GROUP BY 1
),
tb_info_completa_cand AS (
    SELECT
        t1.*,
        COALESCE(t2.total_bens, 0) AS totalBens
    FROM tb_cand AS t1
    LEFT JOIN tb_total_bens AS t2
    ON t1.SQ_CANDIDATO = t2.SQ_CANDIDATO
),
tb_group_uf AS (
    SELECT
        p.SG_PARTIDO,
        p.NM_PARTIDO,
        'GERAL' AS DS_CARGO,
        t1.SG_UF,
        AVG(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS txGeneroFeminino,
        SUM(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS totalGeneroFeminino,
        AVG(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS txCorRacaPreta,
        SUM(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS totalCorRacaPreta,
        AVG(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS txCorRacaNaoBranca,
        SUM(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS totalCorRacaNaoBranca,
        count(*) AS totalCandidatos
    FROM tb_info_completa_cand AS t1
    LEFT JOIN tb_partido_tratado AS p
    ON t1.NR_PARTIDO = p.NR_PARTIDO
    GROUP BY 1, 2, 4
),
tb_group_br AS (
    SELECT
        p.SG_PARTIDO,
        p.NM_PARTIDO,
        'GERAL' AS DS_CARGO,
        'BR' AS SG_UF,
        AVG(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS txGeneroFeminino,
        SUM(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS totalGeneroFeminino,
        AVG(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS txCorRacaPreta,
        SUM(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS totalCorRacaPreta,
        AVG(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS txCorRacaNaoBranca,
        SUM(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS totalCorRacaNaoBranca,
        count(*) AS totalCandidatos
    FROM tb_info_completa_cand AS t1
    LEFT JOIN tb_partido_tratado AS p
    ON t1.NR_PARTIDO = p.NR_PARTIDO
    GROUP BY 1, 2
),
tb_group_cargo_uf AS (
    SELECT
        p.SG_PARTIDO,
        p.NM_PARTIDO,
        t1.DS_CARGO,
        t1.SG_UF,
        AVG(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS txGeneroFeminino,
        SUM(CASE WHEN DS_GENERO = 'FEMININO' THEN 1 ELSE 0 END) AS totalGeneroFeminino,
        AVG(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS txCorRacaPreta,
        SUM(CASE WHEN DS_COR_RACA = 'PRETA' THEN 1 ELSE 0 END) AS totalCorRacaPreta,
        AVG(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS txCorRacaNaoBranca,
        SUM(CASE WHEN DS_COR_RACA NOT IN ('BRANCA', 'NÃO INFORMADO', 'NÃO DIVULGÁVEL') THEN 1 ELSE 0 END) AS totalCorRacaNaoBranca,
        count(*) AS totalCandidatos
    FROM tb_info_completa_cand AS t1
    LEFT JOIN tb_partido_tratado AS p
    ON t1.NR_PARTIDO = p.NR_PARTIDO
    GROUP BY 1, 2, 3, 4
),
tb_group_cargo_br AS (
    SELECT
        SG_PARTIDO,
        NM_PARTIDO,
        DS_CARGO,
        'BR' AS SG_UF,
        1.0 * SUM(totalGeneroFeminino) / SUM(totalCandidatos) AS txGeneroFeminino,
        1.0 * SUM(totalGeneroFeminino) AS totalGeneroFeminino,
        1.0 * SUM(totalCorRacaPreta) / SUM(totalCandidatos) AS txCorRacaPreta,
        1.0 * SUM(totalCorRacaPreta) AS totalCorRacaPreta,
        1.0 * SUM(totalCorRacaNaoBranca) / SUM(totalCandidatos) AS txCorRacaNaoBranca,
        1.0 * SUM(totalCorRacaNaoBranca) AS totalCorRacaNaoBranca,
        SUM(totalCandidatos) AS totalCandidatos
    FROM tb_group_cargo_uf
    GROUP BY 1, 2, 3
),
tb_union_all AS (
    SELECT * FROM tb_group_br

    UNION ALL

    SELECT * FROM tb_group_uf

    UNION ALL

    SELECT * FROM tb_group_cargo_uf

    UNION ALL

    SELECT * FROM tb_group_cargo_br
)

SELECT * FROM tb_union_all;
-- tb_all AS (
--     SELECT
--         SG_PARTIDO,
--         NM_PARTIDO,
--         SUM(CASE WHEN SG_UF = 'AC' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoAC,
--         SUM(CASE WHEN SG_UF = 'AL' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoAL,
--         SUM(CASE WHEN SG_UF = 'AM' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoAM,
--         SUM(CASE WHEN SG_UF = 'AP' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoAP,
--         SUM(CASE WHEN SG_UF = 'BA' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoBA,
--         SUM(CASE WHEN SG_UF = 'CE' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoCE,
--         SUM(CASE WHEN SG_UF = 'ES' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoES,
--         SUM(CASE WHEN SG_UF = 'GO' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoGO,
--         SUM(CASE WHEN SG_UF = 'MA' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoMA,
--         SUM(CASE WHEN SG_UF = 'MG' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoMG,
--         SUM(CASE WHEN SG_UF = 'MS' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoMS,
--         SUM(CASE WHEN SG_UF = 'MT' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoMT,
--         SUM(CASE WHEN SG_UF = 'PA' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoPA,
--         SUM(CASE WHEN SG_UF = 'PB' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoPB,
--         SUM(CASE WHEN SG_UF = 'PE' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoPE,
--         SUM(CASE WHEN SG_UF = 'PI' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoPI,
--         SUM(CASE WHEN SG_UF = 'PR' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoPR,
--         SUM(CASE WHEN SG_UF = 'RJ' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoRJ,
--         SUM(CASE WHEN SG_UF = 'RN' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoRN,
--         SUM(CASE WHEN SG_UF = 'RO' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoRO,
--         SUM(CASE WHEN SG_UF = 'RR' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoRR,
--         SUM(CASE WHEN SG_UF = 'RS' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoRS,
--         SUM(CASE WHEN SG_UF = 'SC' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoSC,
--         SUM(CASE WHEN SG_UF = 'SE' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoSE,
--         SUM(CASE WHEN SG_UF = 'SP' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoSP,
--         SUM(CASE WHEN SG_UF = 'TO' THEN txGeneroFeminino ELSE 0 END) AS txGeneroFemininoTO,
--         1.0 * SUM(1.0 * totalGeneroFeminino) / SUM(totalCandidatos) AS txGeneroFemininoBR,

--         SUM(CASE WHEN SG_UF = 'AC' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaAC,
--         SUM(CASE WHEN SG_UF = 'AL' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaAL,
--         SUM(CASE WHEN SG_UF = 'AM' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaAM,
--         SUM(CASE WHEN SG_UF = 'AP' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaAP,
--         SUM(CASE WHEN SG_UF = 'BA' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaBA,
--         SUM(CASE WHEN SG_UF = 'CE' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaCE,
--         SUM(CASE WHEN SG_UF = 'ES' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaES,
--         SUM(CASE WHEN SG_UF = 'GO' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaGO,
--         SUM(CASE WHEN SG_UF = 'MA' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaMA,
--         SUM(CASE WHEN SG_UF = 'MG' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaMG,
--         SUM(CASE WHEN SG_UF = 'MS' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaMS,
--         SUM(CASE WHEN SG_UF = 'MT' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaMT,
--         SUM(CASE WHEN SG_UF = 'PA' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaPA,
--         SUM(CASE WHEN SG_UF = 'PB' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaPB,
--         SUM(CASE WHEN SG_UF = 'PE' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaPE,
--         SUM(CASE WHEN SG_UF = 'PI' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaPI,
--         SUM(CASE WHEN SG_UF = 'PR' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaPR,
--         SUM(CASE WHEN SG_UF = 'RJ' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaRJ,
--         SUM(CASE WHEN SG_UF = 'RN' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaRN,
--         SUM(CASE WHEN SG_UF = 'RO' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaRO,
--         SUM(CASE WHEN SG_UF = 'RR' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaRR,
--         SUM(CASE WHEN SG_UF = 'RS' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaRS,
--         SUM(CASE WHEN SG_UF = 'SC' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaSC,
--         SUM(CASE WHEN SG_UF = 'SE' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaSE,
--         SUM(CASE WHEN SG_UF = 'SP' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaSP,
--         SUM(CASE WHEN SG_UF = 'TO' THEN txCorRacaPreta ELSE 0 END) AS txCorRacaPretaTO,
--         1.0 * SUM(1.0 * totalCorRacaPreta) / SUM(totalCandidatos) AS txCorRacaPretaBR,

--         SUM(CASE WHEN SG_UF = 'AC' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaAC,
--         SUM(CASE WHEN SG_UF = 'AL' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaAL,
--         SUM(CASE WHEN SG_UF = 'AM' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaAM,
--         SUM(CASE WHEN SG_UF = 'AP' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaAP,
--         SUM(CASE WHEN SG_UF = 'BA' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaBA,
--         SUM(CASE WHEN SG_UF = 'CE' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaCE,
--         SUM(CASE WHEN SG_UF = 'ES' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaES,
--         SUM(CASE WHEN SG_UF = 'GO' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaGO,
--         SUM(CASE WHEN SG_UF = 'MA' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaMA,
--         SUM(CASE WHEN SG_UF = 'MG' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaMG,
--         SUM(CASE WHEN SG_UF = 'MS' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaMS,
--         SUM(CASE WHEN SG_UF = 'MT' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaMT,
--         SUM(CASE WHEN SG_UF = 'PA' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaPA,
--         SUM(CASE WHEN SG_UF = 'PB' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaPB,
--         SUM(CASE WHEN SG_UF = 'PE' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaPE,
--         SUM(CASE WHEN SG_UF = 'PI' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaPI,
--         SUM(CASE WHEN SG_UF = 'PR' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaPR,
--         SUM(CASE WHEN SG_UF = 'RJ' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaRJ,
--         SUM(CASE WHEN SG_UF = 'RN' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaRN,
--         SUM(CASE WHEN SG_UF = 'RO' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaRO,
--         SUM(CASE WHEN SG_UF = 'RR' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaRR,
--         SUM(CASE WHEN SG_UF = 'RS' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaRS,
--         SUM(CASE WHEN SG_UF = 'SC' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaSC,
--         SUM(CASE WHEN SG_UF = 'SE' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaSE,
--         SUM(CASE WHEN SG_UF = 'SP' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaSP,
--         SUM(CASE WHEN SG_UF = 'TO' THEN txCorRacaNaoBranca ELSE 0 END) AS txCorRacaNaoBrancaTO,
--         1.0 * SUM(totalCorRacaNaoBranca) / SUM(totalCandidatos) AS txCorRacaNaoBrancaBR,

--         SUM(totalGeneroFeminino) AS totalGeneroFeminino,
--         SUM(totalCorRacaPreta) AS totalCorRacaPreta,
--         SUM(totalCorRacaNaoBranca) AS totalCorRacaNaoBranca,
--         SUM(totalCandidatos) AS totalCandidatos 
--     FROM tb_group_uf
--     GROUP BY 1, 2
-- )

-- SELECT * FROM tb_all;