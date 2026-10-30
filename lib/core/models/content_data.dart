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
  // Locale-specific preview override for figures whose name genuinely
  // changes across languages (e.g. "Theseus" -> "Thésée" in French),
  // as opposed to accent-only variants which are left untranslated.
  final String? previewFr;
  final String? previewEs;
  // Numéro de mandat pour les présidents multi-mandats
  final int? mandateNumber;
  final String? imageUrl;
  final String? noImageMessage;
  final String? elementSymbol;
  final int? elementAtomicNumber;
  // Warning badge for persons implicated in abuse/violence accusations
  final String? warningText;
  final String? warningLevel; // "red" or "orange"
  // Neutral info badge, e.g. explaining why a coin/seal stands in for a portrait
  final String? imageNote;
  // Shows the localized "dates not documented" note on person cards with no known lifespan
  final bool lifeDatesUndocumented;
  // Terms that must not be translated (e.g. game titles, player names)
  final List<String> protectedTerms;

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
    this.previewFr,
    this.previewEs,
    this.mandateNumber,
    this.imageUrl,
    this.noImageMessage,
    this.elementSymbol,
    this.elementAtomicNumber,
    this.warningText,
    this.warningLevel,
    this.imageNote,
    this.lifeDatesUndocumented = false,
    this.protectedTerms = const [],
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
