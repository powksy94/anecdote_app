/// Converts an ISO 3166-1 alpha-2 country code to its flag emoji using the
/// Unicode regional indicator symbols. Supports "/"-joined dual nationality
/// codes (e.g. "CZ/US" -> 🇨🇿🇺🇸). Returns 🌍 for null/invalid input.
String flagEmoji(String? iso2) {
  if (iso2 == null || iso2.isEmpty) return '🌍';
  return iso2.split('/').map(_singleFlag).join();
}

String _singleFlag(String code) {
  if (code.length != 2) return '🌍';
  final upper = code.toUpperCase();
  return upper.codeUnits
      .map((c) => String.fromCharCode(c - 0x41 + 0x1F1E6))
      .join();
}
