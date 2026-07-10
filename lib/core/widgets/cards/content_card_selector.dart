import 'package:flutter/material.dart';
import '../../models/content_type.dart';
import '../../models/content_data.dart';
import './content_card.dart';
import './image_content_card.dart';
import '../../../features/world/widgets/country_card.dart';
import '../../../features/cinema/widgets/cinema_card.dart';

/// Choisit le widget carte adapté au type de contenu : cinéma, image,
/// géographique (drapeau) ou texte générique — dans cet ordre de priorité.
Widget selectContentCard({
  required ContentType contentType,
  required ContentData? contentData,
  required List<Color> gradient,
  required Color accentColor,
  required String timeUntilMidnight,
}) {
  if (contentType.isCinemaType) {
    return CinemaCard(contentData: contentData, contentType: contentType,
        gradient: gradient, accentColor: accentColor, timeUntilMidnight: timeUntilMidnight);
  }
  // Image-based card takes priority over geo card
  if (contentData?.imageUrl != null || contentData?.noImageMessage != null) {
    return ImageContentCard(contentData: contentData, contentType: contentType,
        gradient: gradient, accentColor: accentColor, timeUntilMidnight: timeUntilMidnight);
  }
  if (contentType.isGeoType) {
    return CountryCard(contentData: contentData, gradient: gradient,
        accentColor: accentColor, timeUntilMidnight: timeUntilMidnight);
  }
  return ContentCard(contentData: contentData, contentType: contentType,
      gradient: gradient, accentColor: accentColor, timeUntilMidnight: timeUntilMidnight);
}
