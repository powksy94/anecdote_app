import '../data/instrument_data.dart';
import '../../../core/models/content_data.dart';

class InstrumentService {
  static List<InstrumentData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadInstruments();
    final i = dailyInstrument(_cache!);

    final buf = StringBuffer();
    buf.writeln('🎻 Family: ${i.family}');
    buf.writeln('🕰️ Origin: ${i.era}');
    buf.writeln('💡 ${i.fact}');

    return ContentData(
      preview: i.name,
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: i.imageUrl,
      noImageMessage: i.noImageMessage,
    );
  }
}
