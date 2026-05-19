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

  ContentData({
    required this.preview,
    this.details = '',
    this.hasDetails = false,
    this.flagSvg,
    this.quoteLang,
    this.quoteEn,
    this.quoteFr,
    this.quoteEs,
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
