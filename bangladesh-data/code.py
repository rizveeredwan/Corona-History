import tabula

# Read pdf into list of DataFrame
#df = tabula.read_pdf("Pdfs/Confirmed COVID-19 cases_upto_21_April 2020_last.pdf", pages='3')
tabula.convert_into("Pdfs/Case_dist_30_May_upload.pdf", "output.csv", output_format="csv", pages='all')
