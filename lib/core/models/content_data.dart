class ContentData {
  final String preview;
  final String details;
  final bool hasDetails;
  final String? flagSvg;

  // Champs spécifiques aux répliques cinéma (VO + traductions officielles)
  final String? quoteLang;
  final String? quoteEn;
  final String? quoteFr;
  final String? quoteEs;
  // Titres du film traduits
  final String? filmTitleFr;
  final String? filmTitleEs;
  final String? filmTitleEn;
  // Numéro de mandat pour les présidents multi-mandats
  final int? mandateNumber;
  final String? imageUrl;
  final String? noImageMessage;
  // Warning badge for persons implicated in abuse/violence accusations
  final String? warningText;
  final String? warningLevel; // "red" or "orange"

  ContentData({
    required this.preview,
    this.details = '',
    this.hasDetails = false,
    this.flagSvg,
    this.quoteLang,
    this.quoteEn,
    this.quoteFr,
    this.quoteEs,
    this.filmTitleFr,
    this.filmTitleEs,
    this.filmTitleEn,
    this.mandateNumber,
    this.imageUrl,
    this.noImageMessage,
    this.warningText,
    this.warningLevel,
  });

  /// Retourne la traduction dans la locale donnée, ou null si VO = locale.
  String? translationFor(String locale) {
    if (quoteLang == null || quoteLang == locale) return null;
    switch (locale) {
      case 'fr': return quoteFr;
      case 'es': return quoteEs;
      default:   return quoteEn;
    }
  }
}
