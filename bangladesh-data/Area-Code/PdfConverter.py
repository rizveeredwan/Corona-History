#-*- coding: utf-8 -*-
import tabula

# Read pdf into list of DataFrame
#df = tabula.read_pdf("Pdfs/Confirmed COVID-19 cases_upto_21_April 2020_last.pdf", pages='3')

tabula.convert_into("DHAKA-26.pdf", "DHAKA.csv", output_format="csv", pages='all')
