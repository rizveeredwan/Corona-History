import tabula

# Read pdf into list of DataFrame
#df = tabula.read_pdf("Pdfs/Confirmed COVID-19 cases_upto_21_April 2020_last.pdf", pages='3')

tabula.convert_into("Pdfs/District_dist_23_april_update.pdf", "output.csv", output_format="csv", pages='all')
