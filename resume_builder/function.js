function generatePDF(){
    const element = document.getElementById("page_content");
    html2pdf().from(element).save();
}