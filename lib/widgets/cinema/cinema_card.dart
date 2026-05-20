import 'package:flutter/material.dart';
import '../../config/env.dart';
import '../../generated/app_localizations.dart';
import '../../models/content_data.dart';
import '../../models/content_type.dart';
import '../../services/translation_service.dart';
import 'cinema_header.dart';
import 'cinema_toggle_section.dart';
import 'cinema_timer_badge.dart';

class CinemaCard extends StatefulWidget {
  final ContentData? contentData;
  final ContentType contentType;
  final List<Color> gradient;
  final Color accentColor;
  final String timeUntilMidnight;

  const CinemaCard({
    super.key,
    required this.contentData,
    required this.contentType,
    required this.gradient,
    required this.accentColor,
    required this.timeUntilMidnight,
  });

  @override
  State<CinemaCard> createState() => _CinemaCardState();
}

class _CinemaCardState extends State<CinemaCard> {
  bool _showDubbing = false;
  bool _showDetails = false;
  String? _translatedContext;
  bool _translatingContext = false;

  Future<void> _translateContext(String locale) async {
    if (_translatingContext || _translatedContext != null) return;
    final raw = widget.contentData?.details ?? '';
    final contextLine = raw.split('\n').where((l) => l.startsWith('📖')).firstOrNull;
    if (contextLine == null || locale == 'en') return;
    final contextText = contextLine.substring(contextLine.indexOf(' ') + 1);
    _translatingContext = true;
    try {
      final ts = TranslationService(apiKey: Env.googleTranslateKey);
      final translated = await ts.translateText(contextText, locale);
      if (mounted) setState(() => _translatedContext = translated);
    } catch (_) {
    } finally {
      _translatingContext = false;
    }
  }

  String? _localFilmTitle(String locale, bool hasDubbing) {
    if (!hasDubbing) return null;
    final d = widget.contentData!;
    switch (locale) {
      case 'fr': return d.filmTitleFr ?? (d.quoteLang != 'fr' ? d.filmTitleEn : null);
      case 'es': return d.filmTitleEs ?? (d.quoteLang != 'es' ? d.filmTitleEn : null);
      default:   return d.filmTitleEn;
    }
  }

  String _localizedDetails(String locale, bool hasDubbing) {
    final raw = widget.contentData?.details ?? '';
    if (!_showDubbing) return raw;
    final lines = raw.split('\n');
    if (lines.isEmpty) return raw;

    // Remplace le titre du film
    final title = _localFilmTitle(locale, hasDubbing);
    if (title != null) {
      final first = lines[0];
      final yearMatch = RegExp(r'\(\d{4}\)').firstMatch(first);
      if (yearMatch != null) {
        final year = yearMatch.group(0)!;
        final typePart = first.contains(' — ') ? first.substring(first.indexOf(' — ')) : '';
        lines[0] = '🎬 $title $year$typePart';
      }
    }

    // Remplace le contexte par la traduction si disponible
    if (_translatedContext != null) {
      for (int i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('📖')) {
          lines[i] = '📖 $_translatedContext';
          break;
        }
      }
    }

    return lines.join('\n');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final locale = Localizations.localeOf(context).languageCode;
    final dubbed = widget.contentData?.translationFor(locale);
    final hasDubbing = dubbed != null && dubbed.isNotEmpty;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            constraints: const BoxConstraints(maxWidth: 400),
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(
                  color: widget.accentColor.withValues(alpha: 0.3),
                  blurRadius: 30,
                  spreadRadius: 5,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              children: [
                CinemaHeader(gradient: widget.gradient, icon: widget.contentType.icon),
                const SizedBox(height: 24),
                Text(
                  widget.contentData?.preview ?? '',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontSize: 20,
                    height: 1.5,
                    fontWeight: FontWeight.w600,
                    fontStyle: FontStyle.italic,
                  ),
                ),
                if (hasDubbing) ...[
                  const SizedBox(height: 16),
                  CinemaToggleSection(
                    label: _showDubbing ? loc.hideDubbing : loc.dubbing,
                    icon: Icons.translate_rounded,
                    accentColor: widget.accentColor,
                    isExpanded: _showDubbing,
                    onTap: () {
                      setState(() {
                        _showDubbing = !_showDubbing;
                        if (_showDubbing) _showDetails = true;
                      });
                      if (_showDubbing) _translateContext(locale);
                    },
                    content: dubbed,
                    contentStyle: theme.textTheme.bodyMedium?.copyWith(
                      height: 1.5,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
                if (widget.contentData?.hasDetails == true) ...[
                  const SizedBox(height: 16),
                  CinemaToggleSection(
                    label: _showDetails ? loc.hideDetails : loc.showDetails,
                    icon: Icons.movie_filter_rounded,
                    accentColor: widget.accentColor,
                    isExpanded: _showDetails,
                    onTap: () => setState(() => _showDetails = !_showDetails),
                    content: _localizedDetails(locale, hasDubbing),
                    contentStyle: theme.textTheme.bodyMedium?.copyWith(height: 1.6),
                  ),
                ],
                const SizedBox(height: 20),
                CinemaTimerBadge(
                  timeUntilMidnight: widget.timeUntilMidnight,
                  accentColor: widget.accentColor,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
