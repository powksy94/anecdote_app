import 'package:flutter/material.dart';
import '../models/content_type.dart';

Widget buildCardDecoration(ContentType type) {
  switch (type) {
    case ContentType.anecdote:
      return Stack(
        children: [
          Positioned(
            top: -20,
            right: -20,
            child: _circle(60, Colors.white.withValues(alpha: 0.1)),
          ),
          Positioned(
            bottom: -30,
            left: -30,
            child: _circle(80, Colors.white.withValues(alpha: 0.08)),
          ),
          Positioned(
            top: 20,
            left: 10,
            child: Icon(Icons.star, size: 12, color: Colors.white.withValues(alpha: 0.3)),
          ),
          Positioned(
            bottom: 40,
            right: 20,
            child: Icon(Icons.star, size: 8, color: Colors.white.withValues(alpha: 0.25)),
          ),
        ],
      );
    case ContentType.chuckNorris:
      return Stack(
        children: [
          Positioned(
            top: -15,
            left: -15,
            child: Transform.rotate(
              angle: 0.3,
              child: _rect(50, 50, Colors.white.withValues(alpha: 0.1)),
            ),
          ),
          Positioned(
            bottom: -20,
            right: -10,
            child: Transform.rotate(
              angle: -0.5,
              child: _rect(40, 40, Colors.white.withValues(alpha: 0.08)),
            ),
          ),
          Positioned(
            top: 15,
            right: 15,
            child: Icon(Icons.bolt, size: 14, color: Colors.white.withValues(alpha: 0.3)),
          ),
        ],
      );
    case ContentType.advice:
      return Stack(
        children: [
          Positioned(
            top: -25,
            right: 20,
            child: _circle(50, Colors.white.withValues(alpha: 0.12)),
          ),
          Positioned(
            bottom: -15,
            left: 30,
            child: _circle(35, Colors.white.withValues(alpha: 0.1)),
          ),
          Positioned(
            top: 40,
            left: 5,
            child: _circle(15, Colors.white.withValues(alpha: 0.15)),
          ),
          Positioned(
            bottom: 30,
            right: 10,
            child: Icon(Icons.format_quote, size: 16, color: Colors.white.withValues(alpha: 0.25)),
          ),
        ],
      );
    case ContentType.history:
      return Stack(
        children: [
          Positioned(
            top: 10,
            right: -20,
            child: Transform.rotate(
              angle: 0.2,
              child: _rect(60, 20, Colors.white.withValues(alpha: 0.1)),
            ),
          ),
          Positioned(
            bottom: 20,
            left: -15,
            child: Transform.rotate(
              angle: -0.15,
              child: _rect(50, 15, Colors.white.withValues(alpha: 0.08)),
            ),
          ),
          Positioned(
            top: 50,
            left: 15,
            child: Icon(Icons.access_time, size: 12, color: Colors.white.withValues(alpha: 0.3)),
          ),
        ],
      );
    case ContentType.animals:
      return Stack(
        children: [
          Positioned(
            top: -10,
            left: 40,
            child: _circle(30, Colors.white.withValues(alpha: 0.12)),
          ),
          Positioned(
            bottom: -25,
            right: -25,
            child: _circle(70, Colors.white.withValues(alpha: 0.08)),
          ),
          Positioned(
            top: 25,
            right: 10,
            child: Icon(Icons.eco, size: 14, color: Colors.white.withValues(alpha: 0.3)),
          ),
          Positioned(
            bottom: 45,
            left: 10,
            child: Icon(Icons.eco, size: 10, color: Colors.white.withValues(alpha: 0.2)),
          ),
        ],
      );
    case ContentType.country:
      return Stack(
        children: [
          Positioned(
            top: -20,
            left: -20,
            child: _circle(70, Colors.white.withValues(alpha: 0.08)),
          ),
          Positioned(
            bottom: -15,
            right: -15,
            child: _circle(55, Colors.white.withValues(alpha: 0.1)),
          ),
          Positioned(
            top: 15,
            right: 12,
            child: Icon(Icons.public, size: 14, color: Colors.white.withValues(alpha: 0.3)),
          ),
          Positioned(
            bottom: 35,
            left: 12,
            child: Icon(Icons.location_on, size: 10, color: Colors.white.withValues(alpha: 0.25)),
          ),
        ],
      );
    case ContentType.exoplanet:
      return Stack(
        children: [
          Positioned(
            top: -20,
            right: -20,
            child: _circle(70, Colors.white.withValues(alpha: 0.07)),
          ),
          Positioned(
            bottom: -15,
            left: -15,
            child: _circle(50, Colors.white.withValues(alpha: 0.09)),
          ),
          Positioned(
            top: 12,
            left: 14,
            child: Icon(Icons.star, size: 8, color: Colors.white.withValues(alpha: 0.3)),
          ),
          Positioned(
            bottom: 30,
            right: 14,
            child: Icon(Icons.star, size: 5, color: Colors.white.withValues(alpha: 0.2)),
          ),
          Positioned(
            top: 40,
            right: 8,
            child: Icon(Icons.star, size: 6, color: Colors.white.withValues(alpha: 0.25)),
          ),
        ],
      );
  }
}

Widget _circle(double size, Color color) => Container(
      width: size,
      height: size,
      decoration: BoxDecoration(shape: BoxShape.circle, color: color),
    );

Widget _rect(double width, double height, Color color) => Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(8),
      ),
    );
