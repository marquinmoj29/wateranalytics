from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

def generar_pdf(resumen_ica, archivo="outputs/reporte_wateranalytics.pdf"):

    doc = SimpleDocTemplate(archivo)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("WaterAnalytics Pro", styles["Title"]))
    story.append(Spacer(1,12))

    story.append(Paragraph("Reporte Ejecutivo Automático", styles["Heading2"]))
    story.append(Spacer(1,12))

    top5 = resumen_ica.head(5)

    for _, row in top5.iterrows():
        txt = f"{row['comunidad_final']} - ICA: {row['ICA_promedio']:.2f} - {row['categoria']}"
        story.append(Paragraph(txt, styles["Normal"]))
        story.append(Spacer(1,6))

    img = "outputs/pca_cluster.png"

    if os.path.exists(img):
        story.append(Spacer(1,12))
        story.append(Image(img, width=500, height=320))

    doc.build(story)

    print("✅ PDF generado:", archivo)