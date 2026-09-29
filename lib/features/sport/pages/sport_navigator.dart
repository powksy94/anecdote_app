import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/cards/hub_split_dialog.dart';
import '../../../core/pages/sub_hub_page.dart';

abstract class SportNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.sportHub,
        leftType: ContentType.sportExploitsHub,
        rightType: ContentType.sportAthletesHub,
        onSelectLeft: () {
          Navigator.of(context, rootNavigator: true).pop();
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.sportExploitsHub,
                categories: const [
                  ContentType.sportRecord,
                  ContentType.sportLegendaryEvent,
                ],
                adService: adService,
              ),
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
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.sportAthletesHub,
                categories: const [
                  ContentType.legendaryAthlete,
                  ContentType.sportGreatWoman,
                  ContentType.sportRivalry,
                ],
                adService: adService,
              ),
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
