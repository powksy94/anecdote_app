import '../../data/american_president_data.dart';
import '../../models/content_data.dart';

class PresidentService {
  static List<AmericanPresidentData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadAmericanPresidents();
    final p = dailyPresident(_cache!);

    final buf = StringBuffer();
    buf.writeln('🔢 Number: ${p.number}${_ordinal(p.number)} President');
    final termEnd = p.termEnd != null ? '${p.termEnd}' : 'present';
    buf.writeln('📅 Term: ${p.termStart} – $termEnd');
    buf.writeln('🏛️ Party: ${p.party}');
    buf.writeln('📍 State: ${p.state}');
    buf.writeln('🤝 Vice President: ${p.vicePresident}');
    buf.writeln('⭐ Famous for: ${p.famousFor}');

    return ContentData(
      preview: '🇺🇸 ${p.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      mandateNumber: p.mandateNumber,
      imageUrl: p.imageUrl,
      noImageMessage: p.noImageMessage,
    );
  }

  String _ordinal(int n) {
    if (n >= 11 && n <= 13) return 'th';
    switch (n % 10) {
      case 1: return 'st';
      case 2: return 'nd';
      case 3: return 'rd';
      default: return 'th';
    }
  }
}
