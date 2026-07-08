import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/hub_split_dialog.dart';
import '../../../core/pages/sub_hub_page.dart';
import './games_hub_page.dart';

abstract class GamingNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.gamingHub,
        leftType: ContentType.gamesHub,
        rightType: ContentType.gamersHub,
        onSelectLeft: () {
          Navigator.pop(context);
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => GamesHubPage(adService: adService),
              transitionsBuilder: (_, animation, __, child) =>
                  FadeTransition(opacity: animation, child: child),
              transitionDuration: const Duration(milliseconds: 250),
            ),
          );
        },
        onSelectRight: () {
          Navigator.pop(context);
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.gamersHub,
                categories: const [
                  ContentType.gamingLegend,
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
