from rest_framework import serializers
from .models import User, Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'host', 'title', 'description', 'property_type',
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms',
            'address', 'city', 'country', 'latitude', 'longitude',
            'amenities', 'is_active', 'created_at', 'updated_at',
            'average_rating', 'total_reviews'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at', 'average_rating', 'total_reviews']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='listing',
        write_only=True
    )
    total_nights = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'user', 'listing', 'listing_id', 'check_in',
            'check_out', 'total_price', 'guests', 'status', 'special_requests',
            'created_at', 'updated_at', 'total_nights'
        ]
        read_only_fields = ['booking_id', 'created_at', 'updated_at', 'total_nights']
    
    def get_total_nights(self, obj):
        return (obj.check_out - obj.check_in).days
    
    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        
        if data['guests'] > data['listing'].max_guests:
            raise serializers.ValidationError(
                f"Number of guests exceeds maximum allowed ({data['listing'].max_guests})"
            )
        
        return data


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'user', 'listing', 'booking', 'rating',
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['review_id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
