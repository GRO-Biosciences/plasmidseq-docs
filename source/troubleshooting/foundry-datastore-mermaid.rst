.. mermaid::

    erDiagram
        plasmidseqrun ||--o{ plasmidseqassembly : ""
        plasmidseqassembly ||--o{ assemblyfeature : ""
        plasmidseqassembly ||--o{ assemblypolymorphism : ""
        assemblypolymorphism ||--o{ featurepolymorphism : ""
        assemblyfeature ||--o{ featurepolymorphism : ""

        assemblyfeature {
            integer id PK
            integer assembly_id FK
            varchar wt_feature_name "Feature name from the template"
            varchar assembly_feature_name "Feature name as determined by the pipeline"
            boolean deleted "TRUE if the feature was wholly comtained in a deleted region"
            integer frameshift_residue "The first residue that institues a frameshift"
            varchar feature_type "The feature type according to GenBank ontology"
            }


        assemblypolymorphism {
            int id PK
            integer assembly_id FK
            integer wt_nt_start "First nucleotide ID of polymorphism when mapped to the template"
            integer wt_nt_end "Last nucleotide ID of polymorphism when mapped to the template"
            integer assembly_nt_start "First nucleotide ID of polymorphism"
            integer assembly_nt_end "First nucleotide ID of polymorphism"
            varchar cds_effect "The mutation or frameshift code caused by the polymorphism, if in a CDS"
            varchar poly_type "insertion | deletion | SNP"
        }

        featurepolymorphism {
            integer feature_id PK, FK
            integer polymorphism_id PK, FK
        }

        plasmidseqassembly {
            integer id PK
            integer run_id FK
            varchar assembly_name "Name of the assembly = {template_name}.{id number}"
            varchar contig_path "The fragment path as determined by the UniCycler assembler"
            integer length "The length of the plasmid in bp"
            double min_prevalence "The ratio of the minimum contig count to the maximum contig count"
            }

        plasmidseqrun {
            integer id PK
            varchar data_id "The sample name"
            varchar experiment_id "The experiment name"
            varchar last_step "The last completed step in the pipeline"
            varchar template_name "The name of the template plasmid in LG"
            varchar basespace_href "The Illumina BaseSpace endpoint used to retrieve FASTQ data"
            varchar error_type "If there was an error, the python class"
            varchar error_message "If there was an error, the associated method"
            varchar error_path "If there was an error, the API endpoint where it happened"
            integer assembly_count "The total number of solutions found by the UniCycler assembler"
            integer template_length "The lenght of the template plasmid in bp"
            double assembly_coverage_mean "The average read coverage as determined by UniCycler"
            double assembly_coverage_std "The standard deviation of coverage as determined by UniCycler"
        }