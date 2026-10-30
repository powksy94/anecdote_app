import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/pages/sub_hub_page.dart';

// Opens the Inventions side directly until the Inventors side has content; this becomes
// a HubSplitDialog (see SportNavigator) once it does.
abstract class TechNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return Navigator.push(
      context,
      PageRouteBuilder(
        pageBuilder: (_, __, ___) => SubHubPage(
          hubType: ContentType.techInventionsHub,
          categories: const [
            ContentType.greatInvention,
          ],
          adService: adService,
        ),
        transitionsBuilder: (_, animation, __, child) =>
            FadeTransition(opacity: animation, child: child),
        transitionDuration: const Duration(milliseconds: 250),
      ),
    );
  }
}
