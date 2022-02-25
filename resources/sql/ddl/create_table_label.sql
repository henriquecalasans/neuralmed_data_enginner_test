CREATE TABLE IF NOT EXISTS neuralmed.label (
    exam_id text,
    classification text,
    labelled_by text,
    labelled_date date,
    labelling_method text,
    classification_type text,
    value boolean);