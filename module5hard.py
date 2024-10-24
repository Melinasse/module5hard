import hashlib
import time


class User:
    """
    Класс содержащий сведения об пользователе: логин, пароль и возраст.
    """

    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.age = age
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def __eq__(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class Video:
    def __init__(self, title: str, duration: int, adult_mode: bool = False):
        self.age = None
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def video_info(self):
        print(f'Заголовок видео: {self.title}, продолжительность (секунд): {self.duration}, '
              f'время остановки: {self.time_now}, возрастное ограничение: {self.adult_mode}')

    def time_stop(self, time_now: int):
        if 0 <= time_now <= self.duration:
            self.time_now = time_now

    def adult_mode_chek(self, age: int):
        if age >= 18:
            self.age = age
        else:
            print('Возрастное ограничение')


class UrTube:

    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname and user.password == password_hash:
                self.current_user = user
                print(f'Добро пожаловать {self.current_user.nickname}')
                return True
        print('Неверный логин или пароль')
        return False

    def register(self, nickname, password, age):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname:
                print(f'Пользователь {nickname} уже существует')
                return
        user_now = User(nickname, password, age)
        self.users.append(user_now)
        self.current_user = user_now
        print(f'Добро пожаловать, уважаемый {self.current_user.nickname}')

    def log_out(self):
        if self.current_user is not None:
            print(f'Пользователь: {self.current_user.nickname}, вышел из системы')
            self.current_user = None
        else:
            print('Нет пользователя')

    def add(self, *videos):
        for video in videos:
            user_new_video = True
            for new_video in self.videos:
                if new_video.title == video.title:
                    user_new_video = False
                    break
            if user_new_video:
                self.videos.append(video)
                print(f'Видео {video.title} добавлено')
            else:
                print(f'Видео {video.title} уже существует')

    def get_videos(self, search):
        search_word_lower = search.lower()
        found = []
        for video in self.videos:
            if search_word_lower in video.title.lower():
                found.append(video.title)
        return found

    def watch_video(self, name):
        if self.current_user is None:
            print('Пожалуйста войдите в аккаунт, чтобы смотреть видео')
            return
        video_watch = None
        for video in self.videos:
            if video.title == name:
                video_watch = video
                break
        if video_watch is None:
            print(f'Видео с названием {name} не найдено.')
            return
        if video_watch.adult_mode and self.current_user.age < 18:
            print('Возрастное ограничение, вам нет 18 лет')
            return
        print(f'Просмотр видео {video_watch.title}')
        while video_watch.time_now < video_watch.duration:
            time.sleep(1)
            video_watch.time_now += 1
            print(f'Время {video_watch.time_now} из {video_watch.duration}')
        if video_watch.time_now == video_watch.duration:
            print('Конец видео')


# Пример использования
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')