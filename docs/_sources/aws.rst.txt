AWS Configuration
=================

Architecture
------------

.. mermaid::

    architecture-beta
        service rtp1(logos:retool-icon)[Basespace Browser]

        group aws(logos:aws)[us east 1]
        service rds(logos:aws-rds)[foundry datastore] in aws

        service api(logos:aws-api-gateway)[plasmid seq] in aws
        service step(logos:aws-step-functions)[PlasmidSeq State Machine] in aws
        service lambda(logos:aws-lambda)[plasmid seq processing] in aws
        service bucket(logos:aws-s3)[foundry plasmid seq] in aws

        rtp1:B -- T:api
        rtp1:R -- T:rds
        api:B -- T:step
        rds:B -- T:lambda
        step:R -- L:lambda
        lambda:R -- L:bucket

        service bs(internet)[Illumina BaseSpace API]

        lambda:B -- T:bs

Resource ARNs
-------------

.. csv-table::
    :file: resources.csv
    :header-rows: 1

Workflow
--------

.. mermaid::

    sequenceDiagram
        actor user as User
        participant rt as Retool
        participant bs as BaseSpace
        participant sf as Step Fuction
        participant rds as RDS
        participant api as API Gateway
        participant lambda as Lambda
        participant s3 as S3 Bucket
        participant lg as LabGuru

        user->>+rt: Select an NGS run
        rt<<->>bs: Query Analyses
        rt->>user: Display options
        user->>rt: Select an Analysis
        rt->>user: Display options
        user->>rt: Select Samples
        rt->>rds: Add samples
        user->>rt: Select PlasmidSeq Run
        rt->>-api: POST /start
        api->>+sf: start
        sf->>api: POST /start_experiment
        api->>lambda: start_expt()
        lambda<<->>rds: get samples
        lambda->>api: return samples
        api->>sf: return samples
        loop SetupMap
            sf->>api: POST /setup
            lambda<<->>bs: get FASTQ files
            lambda<<->>lg: get template GenBank
            lambda->>s3: save sequences
            lambda->>rds: update sample status
            lambda->>api: return sample
            api->>sf: return samples
        end
        loop Map
            sf->>api: POST /trim
            api->>lambda: trim()
            lambda<<->>s3: get FASTQs
            note over lambda: trim FASTQs
            lambda->>s3: save sequences
            lambda->>rds: update sample status
            lambda->>api: return sample
            api->>sf: return samples
            par Assemble Sequences
                sf->>lambda: assemble()
                note over lambda: Assemble Reads
                lambda->>s3: save sequences
                lambda->>rds: add assemblies
                lambda->>rds: update sample status
                lambda->>api: return assemblies
                api->>sf: return assemblies
            and Check Assembly Status
                loop
                    sf->>api: POST /check_transition
                    api<<->>rds: check sample status
                end
            end
            sf->>api: POST /make_plasmids
            api->>lambda: construct_plasmids()
            note over lambda: Build plasmids from assembly paths
            lambda->>s3: save sequences
            lambda->>rds: update sample status
            lambda->>api: return assemblies
            api->>sf: return assemblies
            loop
                sf->>api: POST /transfer_annotations
                api->>lambda: transfer_annotations()
                note over lambda: align assembly to template
                note over lambda: copy annotations
                note over lambda: determine mutations
                lambda->>s3: save sequences
                lambda->>rds: add polymorphisms and features
                lambda->>rds: update sample status
                lambda->>api: return assemblies
                api->>sf: return assemblies
            end
        end
        sf->>lambda: combine()
        lambda<<->>rds: get sample/assembly details
        note over lambda: complile data to XLSX
        lambda<<->>s3: get assembly GenBanks
        note over lambda: zip data and sequences
        lambda->>s3: save zip file
        lambda->>sf: return samples
        deactivate sf
        user<<->>+rt: check status
        user->>rt: request data
        rt->>-api: GET /zipfile
        api->>user: download results

