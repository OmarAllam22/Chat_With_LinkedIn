function generatePDF(){
    const element = document.getElementsByClassName("page_content");
    html2pdf().from(element).save();
}