class ContentData {
  final String preview;
  final String details;
  final bool hasDetails;

  ContentData({
    required this.preview,
    this.details = '',
    this.hasDetails = false,
  });
}
