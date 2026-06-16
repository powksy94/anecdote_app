import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/hub_split_dialog.dart';
import '../../../core/pages/sub_hub_page.dart';

abstract class ArtNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.artHub,
        leftType: ContentType.artWorksHub,
        rightType: ContentType.artArtistsHub,
        onSelectLeft: () {
          Navigator.pop(context);
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.artWorksHub,
                categories: const [
                  ContentType.painting,
                  ContentType.sculpture,
                  ContentType.architecture,
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
          Navigator.pop(context);
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.artArtistsHub,
                categories: const [
                  ContentType.famousArtist,
                  ContentType.photographer,
                  ContentType.classicalComposer,
                  ContentType.nobelPrize,
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
