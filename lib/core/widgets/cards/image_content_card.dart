import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../../models/content_data.dart';
import '../../models/content_type.dart';
import '../../../features/cinema/widgets/cinema_toggle_section.dart';
import '../../../features/cinema/widgets/cinema_timer_badge.dart';
import '../badges/warning_badge.dart';
import '../badges/info_note_badge.dart';
import '../layout/image_header.dart';

class ImageContentCard extends StatefulWidget {
  final ContentData? contentData;
  final ContentType contentType;
  final List<Color> gradient;
  final Color accentColor;
  final String timeUntilMidnight;

  const ImageContentCard({
    super.key,
    required this.contentData,
    required this.contentType,
    required this.gradient,
    required this.accentColor,
    required this.timeUntilMidnight,
  });

  @override
  State<ImageContentCard> createState() => _ImageContentCardState();
}

class _ImageContentCardState extends State<ImageContentCard> {
  bool _showDetails = false;

  static const _personTypes = {
    ContentType.famousArtist,
    ContentType.photographer,
    ContentType.classicalComposer,
    ContentType.nobelPrize,
    ContentType.kingOfFrance,
    ContentType.americanPresident,
    ContentType.lgbtqiaPersonality,
    ContentType.pioneerWoman,
    ContentType.legendaryAthlete,
    ContentType.gamingLegend,
  };

  static const _copyrightTypes = {
    ContentType.painting,
    ContentType.sculpture,
  };

  String? _nimText(AppLocalizations loc) {
    switch (widget.contentType) {
      case ContentType.exoplanet:
        return widget.contentData?.noImageMessage != null ? loc.noImageExoplanet : null;
      case ContentType.star:
        return widget.contentData?.noImageMessage != null ? loc.noImageStar : null;
      case ContentType.spaceMission:
        return widget.contentData?.noImageMessage != null ? loc.noImageSpaceMission : null;
      case ContentType.lgbtqiaPersonality:
        return widget.contentData?.noImageMessage != null ? loc.noImageLgbtqia : null;
      case ContentType.pioneerWoman:
        return widget.contentData?.noImageMessage != null ? loc.noImagePioneerWoman : null;
      case ContentType.legendaryAthlete:
        return widget.contentData?.noImageMessage != null ? loc.noImageLegendaryAthlete : null;
      case ContentType.gamingLegend:
        return widget.contentData?.noImageMessage != null ? loc.noImageGamingLegend : null;
      case ContentType.classicGame:
        return widget.contentData?.noImageMessage != null ? loc.noImageClassicGame : null;
      case ContentType.gamingNomination:
        return widget.contentData?.noImageMessage != null ? loc.noImageGamingNomination : null;
      case ContentType.worstGame:
        return widget.contentData?.noImageMessage != null ? loc.noImageWorstGame : null;
      case ContentType.bannedGame:
        return widget.contentData?.noImageMessage != null ? loc.noImageBannedGame : null;
      case ContentType.insect:
        // Toujours disponible : l'URL Wikipedia peut échouer silencieusement
        return loc.noImageGeneric;
      default:
        return widget.contentData?.noImageMessage != null ? loc.noImageGeneric : null;
    }
  }

  static const _containTypes = {
    ContentType.sculpture,
    ContentType.architecture,
    ContentType.humanBone,
    ContentType.dinosaur,
    ContentType.animals,
    ContentType.frenchDepartment,
    ContentType.mineral,
    ContentType.bird,
    ContentType.solarSystemMoon,
    ContentType.nobelPrize,
    ContentType.painting,
    ContentType.spaceMission,
    ContentType.star,
    ContentType.exoplanet,
    ContentType.chemicalElement,
    ContentType.battle,
    ContentType.frenchCommune,
    ContentType.americanState,
    ContentType.volcano,
    ContentType.insect,
    ContentType.desert,
    ContentType.river,
    ContentType.sea,
  };

  Alignment get _imageAlignment => _personTypes.contains(widget.contentType)
      ? const Alignment(0, -0.5)
      : Alignment.center;

  double get _imageHeight => _personTypes.contains(widget.contentType) ? 280 : 200;

  BoxFit get _boxFit => _containTypes.contains(widget.contentType)
      ? BoxFit.contain
      : BoxFit.cover;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            constraints: const BoxConstraints(maxWidth: 400),
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
                ImageHeader(
                  imageUrl: widget.contentData?.imageUrl,
                  gradient: widget.gradient,
                  fallbackIcon: widget.contentType.icon,
                  noImageMessage: _nimText(loc),
                  noImageTitle: loc.noImageTitle,
                  noImageExplanation: widget.contentData?.noImageMessage != null &&
                      _copyrightTypes.contains(widget.contentType)
                      ? loc.noImageExplanation
                      : null,
                  elementSymbol: widget.contentData?.elementSymbol,
                  elementAtomicNumber: widget.contentData?.elementAtomicNumber,
                  imageAlignment: _imageAlignment,
                  height: _imageHeight,
                  boxFit: _boxFit,
                ),
                Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Flexible(
                            child: Text(
                              widget.contentData?.preview ?? '',
                              textAlign: TextAlign.center,
                              style: theme.textTheme.titleLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                                height: 1.3,
                              ),
                            ),
                          ),
                          if (widget.contentData?.warningText != null) ...[
                            const SizedBox(width: 8),
                            WarningBadge(
                              text: widget.contentData!.warningText!,
                              level: widget.contentData!.warningLevel ?? 'orange',
                            ),
                          ],
                          if (widget.contentData?.imageNote != null) ...[
                            const SizedBox(width: 8),
                            InfoNoteBadge(text: widget.contentData!.imageNote!),
                          ],
                        ],
                      ),
                      if (widget.contentData?.hasDetails == true) ...[
                        const SizedBox(height: 16),
                        CinemaToggleSection(
                          label: _showDetails ? loc.hideDetails : loc.showDetails,
                          icon: Icons.visibility_rounded,
                          accentColor: widget.accentColor,
                          isExpanded: _showDetails,
                          onTap: () => setState(() => _showDetails = !_showDetails),
                          content: widget.contentData?.details ?? '',
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
          ),
        ],
      ),
    );
  }
}
