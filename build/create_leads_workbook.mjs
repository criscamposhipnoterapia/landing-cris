import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "outputs/pre_deploy_cris";
await fs.mkdir(outputDir, { recursive: true });

const workbook = Workbook.create();

const resumo = workbook.worksheets.add("Resumo");
const leads = workbook.worksheets.add("Leads");
const upload = workbook.worksheets.add("Upload Google Ads");
const instrucoes = workbook.worksheets.add("Instrucoes");

for (const sheet of [resumo, leads, upload, instrucoes]) {
  sheet.showGridLines = false;
}

const brand = "#5E2616";
const ink = "#2C2521";
const cream = "#F3EDE3";
const light = "#FBF7F0";
const clay = "#9A7B4F";
const terra = "#A86B4C";
const border = "#E3D7C8";
const inputFill = "#FFF7D6";

function styleTitle(range) {
  range.format = {
    fill: brand,
    font: { bold: true, color: "#FFFFFF", size: 15 },
    alignment: { horizontal: "left", vertical: "center" },
  };
}

function styleHeader(range) {
  range.format = {
    fill: cream,
    font: { bold: true, color: ink },
    borders: { preset: "all", style: "thin", color: border },
    alignment: { vertical: "center" },
  };
}

function styleTable(range) {
  range.format = {
    fill: "#FFFFFF",
    borders: { preset: "all", style: "thin", color: "#EEE5DA" },
    alignment: { vertical: "top" },
  };
}

// Resumo
resumo.getRange("A1:F1").merge();
resumo.getRange("A1").values = [["FASE 0 - Fonte de verdade"]];
styleTitle(resumo.getRange("A1:F1"));
resumo.getRange("A3:B8").values = [
  ["Metrica", "Valor"],
  ["Total de leads registrados", null],
  ["Leads com click ID", null],
  ["% leads com click ID", null],
  ["Sessoes de Clareza pagas", null],
  ["Processos fechados", null],
];
styleHeader(resumo.getRange("A3:B3"));
styleTable(resumo.getRange("A4:B8"));
resumo.getRange("B4").formulas = [["=COUNTA(Leads!A2:A501)"]];
resumo.getRange("B5").formulas = [["=SUM(Leads!W2:W501)"]];
resumo.getRange("B6").formulas = [["=IF(B4=0,0,B5/B4)"]];
resumo.getRange("B7").formulas = [["=COUNTIF(Leads!O2:O501,\"Sessao de Clareza paga\")"]];
resumo.getRange("B8").formulas = [["=COUNTIF(Leads!O2:O501,\"Processo fechado\")"]];
resumo.getRange("B6").format.numberFormat = "0.0%";
resumo.getRange("A10:F13").values = [
  ["Regra de pronto", "Acima de 90% dos leads novos com gclid, gbraid ou wbraid registrado.", null, null, null, null],
  ["Rotina", "Registrar cada conversa nova do WhatsApp e atualizar status quando pagar Clareza ou fechar Processo.", null, null, null, null],
  ["Google Ads", "Criar as conversoes offline antes do primeiro upload e usar nomes exatamente iguais aos da conta.", null, null, null, null],
  ["Observacao", "A aba de upload nao deve receber telefone ou dados pessoais, a menos que a conta esteja configurada para enhanced conversions.", null, null, null, null],
];
resumo.getRange("A10:A13").format = { font: { bold: true, color: brand }, fill: light };
resumo.getRange("B10:F13").merge(true);
resumo.getRange("B10:F13").format = { fill: light, borders: { preset: "all", style: "thin", color: border }, wrapText: true };
resumo.getRange("A:A").format.columnWidth = 28;
resumo.getRange("B:F").format.columnWidth = 22;

// Leads
const leadHeaders = [
  "data_hora_lead",
  "telefone",
  "nome",
  "pagina_origem",
  "gclid",
  "gbraid",
  "wbraid",
  "click_id_para_google",
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
  "primeira_mensagem_whatsapp",
  "status",
  "data_sessao_clareza",
  "valor_sessao_clareza",
  "data_processo_fechado",
  "valor_processo",
  "observacoes",
  "proxima_acao",
  "responsavel",
  "tem_click_id",
];
leads.getRange("A1:W1").values = [leadHeaders];
styleHeader(leads.getRange("A1:W1"));
styleTable(leads.getRange("A2:W501"));
leads.getRange("H2").formulas = [["=IF(E2<>\"\",E2,IF(F2<>\"\",F2,IF(G2<>\"\",G2,\"\")))"]];
leads.getRange("H2:H501").fillDown();
leads.getRange("W2").formulas = [["=IF(H2<>\"\",1,0)"]];
leads.getRange("W2:W501").fillDown();
leads.getRange("A2:A501").format.numberFormat = "yyyy-mm-dd hh:mm";
leads.getRange("P2:P501").format.numberFormat = "yyyy-mm-dd";
leads.getRange("R2:R501").format.numberFormat = "yyyy-mm-dd";
leads.getRange("Q2:Q501").format.numberFormat = "\"R$\" #,##0.00";
leads.getRange("S2:S501").format.numberFormat = "\"R$\" #,##0.00";
leads.getRange("A:W").format.wrapText = true;
leads.getRange("A:A").format.columnWidth = 18;
leads.getRange("B:C").format.columnWidth = 18;
leads.getRange("D:D").format.columnWidth = 16;
leads.getRange("E:H").format.columnWidth = 26;
leads.getRange("I:M").format.columnWidth = 18;
leads.getRange("N:N").format.columnWidth = 38;
leads.getRange("O:O").format.columnWidth = 24;
leads.getRange("P:S").format.columnWidth = 18;
leads.getRange("T:V").format.columnWidth = 26;
leads.getRange("W:W").format.columnWidth = 12;
leads.freezePanes.freezeRows(1);
leads.getRange("D2:D501").dataValidation = { rule: { type: "list", values: ["ansiedade", "burnout", "medos", "site"] } };
leads.getRange("O2:O501").dataValidation = { rule: { type: "list", values: ["Novo lead", "Contato feito", "Sessao de Clareza paga", "Processo fechado", "Perdido"] } };
leads.getRange("A2:W501").conditionalFormats.add("containsText", {
  text: "Processo fechado",
  format: { fill: "#E7F3E4", font: { color: "#2C2521" } },
});
leads.getRange("A2:W501").conditionalFormats.add("containsText", {
  text: "Perdido",
  format: { fill: "#F8E7E0", font: { color: "#2C2521" } },
});

// Upload Google Ads
upload.getRange("A1:F1").merge();
upload.getRange("A1").values = [["Modelo base para upload offline - usar o template final da propria conta Google Ads"]];
styleTitle(upload.getRange("A1:F1"));
upload.getRange("A3:F3").values = [["Google Click ID", "Conversion Name", "Conversion Time", "Order ID", "Conversion Value", "Conversion Currency"]];
styleHeader(upload.getRange("A3:F3"));
styleTable(upload.getRange("A4:F203"));
upload.getRange("A4:F6").values = [
  ["", "Sessao de Clareza paga", "2026-06-28 14:30:00-0300", "", "", "BRL"],
  ["", "Processo fechado", "2026-06-28 14:30:00-0300", "", "", "BRL"],
  ["", "", "", "", "", ""],
];
upload.getRange("A4:F5").format = { fill: inputFill, borders: { preset: "all", style: "thin", color: border }, wrapText: true };
upload.getRange("A:A").format.columnWidth = 34;
upload.getRange("B:B").format.columnWidth = 26;
upload.getRange("C:C").format.columnWidth = 25;
upload.getRange("D:D").format.columnWidth = 18;
upload.getRange("E:F").format.columnWidth = 20;
upload.getRange("E4:E203").format.numberFormat = "#,##0.00";
upload.freezePanes.freezeRows(3);

// Instrucoes
instrucoes.getRange("A1:D1").merge();
instrucoes.getRange("A1").values = [["Como usar esta planilha"]];
styleTitle(instrucoes.getRange("A1:D1"));
instrucoes.getRange("A3:D12").values = [
  ["Passo", "O que fazer", "Quando", "Observacao"],
  ["1", "Copiar da primeira mensagem do WhatsApp o telefone, a pagina de origem e o ID em [ref: ...].", "Quando o lead entra", "Se aparecer [ref: gclid:XYZ], preencher gclid. Se aparecer gbraid ou wbraid, preencher a coluna correspondente."],
  ["2", "Registrar UTMs quando aparecerem na URL ou no sistema de campanha.", "No cadastro do lead", "O codigo da landing ja preserva utm_source, utm_medium, utm_campaign, utm_term e utm_content."],
  ["3", "Atualizar o status do lead.", "A cada avanco", "Novo lead > Contato feito > Sessao de Clareza paga > Processo fechado ou Perdido."],
  ["4", "Preencher valor e data quando houver pagamento.", "Na venda", "Usar valor real recebido/contratado, nao estimativa."],
  ["5", "Preparar a aba Upload Google Ads somente depois de criar as conversoes offline na conta.", "Semanalmente", "O nome da conversao deve ser exatamente igual ao nome criado no Google Ads."],
  ["6", "Nao enviar telefone ou dados pessoais no upload simples de GCLID.", "No upload", "Dados pessoais so devem ir em enhanced conversions e com a configuracao correta."],
  ["7", "Meta de pronto da FASE 0.", "Semanalmente", "Resumo deve mostrar mais de 90% de leads com click ID gravado."],
  ["Fonte Google", "https://support.google.com/google-ads/answer/7012522", "Referencia", "Capturar GCLID e armazenar junto aos dados do prospect."],
  ["Fonte Google", "https://support.google.com/google-ads/answer/7014069", "Referencia", "Campos de upload: Google Click ID, Conversion Name, Conversion Time, Conversion Value e Currency."],
];
styleHeader(instrucoes.getRange("A3:D3"));
styleTable(instrucoes.getRange("A4:D12"));
instrucoes.getRange("A:A").format.columnWidth = 18;
instrucoes.getRange("B:B").format.columnWidth = 52;
instrucoes.getRange("C:C").format.columnWidth = 18;
instrucoes.getRange("D:D").format.columnWidth = 58;
instrucoes.getRange("A3:D12").format.wrapText = true;

for (const [name, range] of [
  ["resumo", "A1:F13"],
  ["leads", "A1:V16"],
  ["upload", "A1:F12"],
  ["instrucoes", "A1:D12"],
]) {
  const preview = await workbook.render({ sheetName: name === "resumo" ? "Resumo" : name === "leads" ? "Leads" : name === "upload" ? "Upload Google Ads" : "Instrucoes", range, scale: 1, format: "png" });
  await fs.writeFile(`${outputDir}/preview_${name}.png`, new Uint8Array(await preview.arrayBuffer()));
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/Modelo_Rastreio_Leads_Cris.xlsx`);
console.log(`${outputDir}/Modelo_Rastreio_Leads_Cris.xlsx`);
