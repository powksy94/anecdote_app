import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/cards/hub_split_dialog.dart';
import '../../../core/pages/sub_hub_page.dart';
import 'science_living_page.dart';

abstract class ScienceNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.scienceHub,
        leftType: ContentType.scienceLivingHub,
        rightType: ContentType.scienceNonLivingHub,
        onSelectLeft: () {
          Navigator.of(context, rootNavigator: true).pop();
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => ScienceLivingPage(adService: adService),
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
                hubType: ContentType.scienceNonLivingHub,
                categories: const [
                  ContentType.chemicalElement,
                  ContentType.mineral,
                  ContentType.cloud,
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
