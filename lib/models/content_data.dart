class ContentData {
  final String preview;
  final String details;
  final bool hasDetails;
  final String? flagSvg;

  ContentData({
    required this.preview,
    this.details = '',
    this.hasDetails = false,
    this.flagSvg,
  });
}
