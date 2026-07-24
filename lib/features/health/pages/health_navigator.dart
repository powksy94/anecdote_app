import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../generated/app_localizations.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/cards/hub_split_dialog.dart';
import './health_general_page.dart';
import './mental_health_page.dart';

abstract class HealthNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (dialogCtx) {
        final loc = AppLocalizations.of(dialogCtx)!;
        return AlertDialog(
          title: Text(loc.healthInfoTitle),
          content: Text(loc.healthInfoMessage),
          actions: [
            ElevatedButton(
              onPressed: () {
                Navigator.pop(dialogCtx);
                _showSplit(context, adService);
              },
              child: Text(loc.healthInfoAcknowledge),
            ),
          ],
        );
      },
    );
  }

  static void _showSplit(BuildContext context, AdService adService) {
    showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.healthHub,
        leftType: ContentType.healthGeneralHub,
        rightType: ContentType.mentalHealthHub,
        onSelectLeft: () {
          Navigator.of(context, rootNavigator: true).pop();
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => HealthGeneralPage(adService: adService),
              transitionsBuilder: (_, animation, __, child) =>
                  FadeTransition(opacity: animation, child: child),
              transitionDuration: const Duration(milliseconds: 250),
            ),
          );
        },
        onSelectRight: () {
          Navigator.of(context, rootNavigator: true).pop();
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => MentalHealthPage(adService: adService),
              transitionsBuilder: (_, animation, __, child) =>
                  FadeTransition(opacity: animation, child: child),
              transitionDuration: const Duration(milliseconds: 250),
            ),
          );
        },
      ),
    );
  }
}
