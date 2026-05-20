import '../data/cinema_quote_data.dart';
import '../models/content_data.dart';
import '../models/content_type.dart';

class CinemaService {
  final ContentType type;
  CinemaService(this.type);

  Future<ContentData> getDailyContent() async {
    final quotes = await loadCinemaQuotes(type);
    final q = dailyCinemaQuote(quotes, type);

    final details = [
      '🎬 ${q.film} (${q.year})${q.type != null ? " — ${_typeLabel(q.type!)}" : ""}',
      '🎭 ${q.character}',
      '👤 ${q.actor}',
      '🎥 ${q.director}',
      '⏱️ ${q.timing}',
      '📖 ${q.context}',
    ].join('\n');

    return ContentData(
      preview: '"${q.quote}"',
      details: details,
      hasDetails: true,
      quoteLang: q.quoteLang,
      quoteEn: q.qEn,
      quoteFr: q.qFr,
      quoteEs: q.qEs,
      filmTitleFr: q.fiFr,
      filmTitleEs: q.fiEs,
      filmTitleEn: q.fiEn,
    );
  }

  String _typeLabel(String type) {
    switch (type) {
      case 'remake':   return 'Remake';
      case 'sequel':   return 'Sequel';
      case 'prequel':  return 'Prequel';
      case 'spin-off': return 'Spin-off';
      case 'reissue':  return 'Reissue';
      default:         return type;
    }
  }
}
