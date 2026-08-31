WITH tb_cand AS (
    SELECT 
        SQ_CANDIDATO,
        SG_UF,
        DS_CARGO,
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
        COLAESCE(t2.totalBens, 0) AS totalBens
    FROM tb_cand as t1
    LEFT JOIN tb_total_bens AS t2
    ON t1.SQ_CANDIDATO = t2.SQ_CANDIDATO
)