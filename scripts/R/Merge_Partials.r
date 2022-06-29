#! /usr/local/bin/Rscript

# The Purpose of this script is to combine CSV files that are in multiple files
files <- list.files('../../data_docs/')

files <- files[ stringr::str_detect(files, "[:digit:]_of_[:digit:]") ]

out_files_term <- stringr::str_remove( files[ stringr::str_detect(files, "[:digit:]_of_[:digit:].csv") ], 
                                       "[:digit:]_of_[:digit:].csv" 
                                      )
out_files_nonterm <- stringr::str_remove( files[ stringr::str_detect(files, "_[:digit:]_of_[:digit:]_") ], 
                                          "[:digit:]_of_[:digit:]" 
)

out_files_term <- out_files_term[!duplicated(out_files_term)]
out_files_nonterm <- out_files_nonterm[!duplicated(out_files_nonterm)]

for(path in out_files_term ){
  targets <- paste0( '../../data_docs/',
                     files[ stringr::str_detect(
                       files, 
                       stringr::str_c(path,"[:digit:]_of_[:digit:].csv")
                      ) ]
  )
  loaded <- lapply(targets, read.csv)
  merged <- dplyr::bind_rows(loaded, .id = "column_label")
  outpath <- paste0(
    '../../data_docs/', 
    gsub( "_$", '', path),
    '.csv')
  write.csv( merged, file = outpath, row.names = F)
}

for(path in out_files_nonterm ){
  targets <- paste0( '../../data_docs/',
                     files[ stringr::str_detect(
                       files, 
                       stringr::str_replace(path, '__', "_[:digit:]_of_[:digit:]_")
                     )]
  )
  loaded <- lapply(targets, read.csv)
  merged <- dplyr::bind_rows(loaded, .id = "column_label")
  outpath <- paste0(
    '../../data_docs/', 
    gsub(
      '__',
      '_',
      gsub( "_.csv", '.csv', path)
    )
  )
  write.csv( merged, file = outpath, row.names = F)
}

# Move Old files:
dir.create('../../data_docs/deprecated')
for( fil in files){
  ori <- paste0('../../data_docs/',fil)
  system(paste0( 'mv ', ori, ' ../../data_docs/deprecated/'))
}

