import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import 'update_popup_button.dart';

class UpdatePopupContent extends StatelessWidget {
  final AppLocalizations loc;
  final AnimationController shimmerCtrl;
  final bool isUpdating;
  final VoidCallback onUpdate;
  final VoidCallback? onLater;

  const UpdatePopupContent({
    super.key,
    required this.loc,
    required this.shimmerCtrl,
    required this.isUpdating,
    required this.onUpdate,
    this.onLater,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          loc.updateTitle,
          textAlign: TextAlign.center,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 22,
            fontWeight: FontWeight.bold,
            height: 1.3,
            letterSpacing: -0.3,
          ),
        ),
        const SizedBox(height: 10),
        Text(
          loc.updateMessage,
          textAlign: TextAlign.center,
          style: const TextStyle(
            color: Color(0xFFB0B8D8),
            fontSize: 14,
            height: 1.65,
          ),
        ),
        const SizedBox(height: 32),
        UpdateShimmerButton(
          label: loc.updateButton,
          shimmerCtrl: shimmerCtrl,
          isLoading: isUpdating,
          onTap: onUpdate,
        ),
        if (onLater != null) ...[
          const SizedBox(height: 8),
          TextButton(
            onPressed: isUpdating ? null : onLater,
            style: TextButton.styleFrom(
              foregroundColor: const Color(0xFF6B7280),
            ),
            child: Text(loc.updateLaterButton),
          ),
        ],
      ],
    );
  }
}
