import '../data/gaming_anecdote_data.dart';
import '../../../core/models/content_data.dart';

class GamingAnecdoteService {
  static List<GamingAnecdoteData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadGamingAnecdotes();
    final a = dailyGamingAnecdote(_cache!);
    return ContentData(
      preview: a.fact,
      details: '',
      hasDetails: false,
    );
  }
}
