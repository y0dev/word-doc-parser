import math

class TimeToRead:
    def __init__(self, word_count: int):
        self._secs = ""
        self._mins = ""
        self._hours = ""
        self.__calculate_time_to_read(word_count)

    def __convert_to_preferred_format(self, seconds):
        sec = seconds % (24 * 3600)
        dec_hour = math.floor(sec / 3600)
        sec %= 3600
        dec_min = math.floor(sec / 60)
        sec %= 60
        
        # Assigning the formatted time values
        self._secs = str(int(sec))
        self._mins = str(int(dec_min))
        self._hours = str(int(dec_hour))

    def __calculate_time_to_read(self, word_count):
        WORDS_PER_MINUTE = 250
        MINUTE = 60
        HOUR = 60 * MINUTE  # 3600 seconds
        
        time_to_read_mins = (word_count / WORDS_PER_MINUTE) * MINUTE

        self.__convert_to_preferred_format(time_to_read_mins)
    
    def get_time_as_obj(self):
        # Return the time as a dictionary
        return {
            "hours": self._hours,
            "minutes": self._mins,
            "seconds": self._secs
        }

if __name__ == "__main__":
    # Example usage:
    word_count = 1000
    time_to_read = TimeToRead(word_count)

    print(f"Hours: {time_to_read._hours}, Minutes: {time_to_read._mins}, Seconds: {time_to_read._secs}")
