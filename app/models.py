from django.db import models
from django.contrib.auth.models import User

class PlaceOfWork(models.Model):
    place = models.CharField("就業場所", max_length=100)

    def __str__(self):
        return self.place

class Company(models.Model):
    # 基本情報
    name = models.CharField("会社名", max_length=200)
    url = models.URLField("会社URL")
    employee_count = models.IntegerField("社員数")
    
    # 勤務条件
    working_hours = models.TextField("就業時間", default='')
    place_of_work = models.ManyToManyField(PlaceOfWork, verbose_name="就業場所")
    overtime = models.IntegerField("平均残業時間")
    salary = models.IntegerField("基本給")
    allowance = models.TextField("諸手当", default='特になし')
    salary_increase = models.CharField("昇給", max_length=200)
    bonuses = models.CharField("賞与", max_length=200, default='')
    holidays_and_vacations = models.CharField("休日休暇", max_length=200, default='')
    paid_leave_utilization_rate = models.IntegerField("有休消化率")
    
    # 福利厚生
    employee_benefits = models.TextField("福利厚生")
    
    # エンジニアリング領域
    class Engineering_Field(models.TextChoices):
        FRONTENDENGINEER = 'frontend_engineer', 'フロントエンジニア(ウェブ開発) - デザインと実装を担当。HTML, CSS, JavaScriptを使用して、ユーザーが直接触れる部分を作成する。'
        BACKENDENGINEER = 'backend_engineer', 'バックエンドエンジニア(ソフトウェア開発、データベース管理) - ロジックやデータベースの設計・実装を担当。APIの設計やデータ処理、サーバーの運用管理を行う。'
        FULLSTACKENGINEER = 'fullstack_engineer', 'フルスタックエンジニア(フロントとバックエンドのハーフ) - ウェブアプリケーション全体の設計と実装を担当。幅広い技術スキルが求められる。'
        DEVEOPMENTSENGINEER = 'deveopments_engineer', 'デベロップメントエンジニア(ソフトウェア開発、プログラミング) - ソフトウェアの設計・開発を担当。基本的にはプログラミング全般に関わる。'
        SITERELIABILITYENGINEER = 'sitereliability_engineer', 'サイトリライアビリティエンジニア(システム管理、クラウドコンピューティング、ネットワークエンジニアリング、セキュリティ) - システムの運用と監視を行い、障害対応やパフォーマンスの最適化に注力すする。'
        UNKNOWN = 'unknown', '不明'
    engineering_field = models.CharField("エンジニア領域", choices=Engineering_Field.choices, max_length=50)
    
    # 使用言語
    class Programming_Language(models.TextChoices):
        PYTHON = 'python', 'Python'
        JAVA = 'java', 'Java'
        GO = 'go', 'Go'
        MISCELIANEOUS = 'miscellaneous', 'その他'
    programming_language = models.CharField("使用言語", choices=Programming_Language.choices, max_length=50)
    
    # 研修制度
    class Training(models.TextChoices):
        YES = 'yes', 'あり'
        NO = 'no', 'なし'
    training = models.CharField("研修制度", choices=Training.choices, max_length=10)
    
    # 働き方
    class Ways_Of_Working(models.TextChoices):
        FLEX_TIME = 'flex_time', 'フレックスタイム制 - 働く時間を柔軟に調整できる制度'
        SHORT_HOURS = 'short_hours', '時短勤務 - 通常の労働時間より短い勤務時間'
        SHIFT_WORK = 'shift_work', 'シフト勤務 - 複数のシフトを組み合わせて勤務する方法'
        CORE_TIME = 'core_time', 'コアタイム制 - 一部の時間帯は必ず勤務することが求められる制度'
        REMOTE_WORK = 'remote_work', 'テレワーク - 自宅やその他のリモートな場所からの勤務'
        HYBRID_WORK = 'hybrid_work', 'ハイブリッド勤務 - オフィスとリモートの両方を組み合わせて働く方法'
        FREE_ADDRESS = 'free_address', 'フリーアドレス - 自由な座席を選べるオフィス勤務の形態'
        PART_TIME = 'part_time', 'パートタイム勤務 - 通常のフルタイムより短い勤務時間で働く方法'
        DISCRETIONARY_WORK = 'discretionary_work', '裁量労働制 - 労働時間の裁量が社員に委ねられる制度'
        DIGITAL_NOMAD = 'digital_nomad', 'デジタルノマド - インターネットを利用して世界中どこでも働くスタイル'
    ways_of_working = models.CharField("働き方", choices=Ways_Of_Working.choices, max_length=18, default='flex_time')    
    
    # 成長環境
    class Growth_Environment(models.TextChoices):
        FIVE = 'five', '★★★★★(忙しい)'
        FOUR = 'four', '★★★★'
        THREE = 'three', '★★★'
        TWO = 'two', '★★'
        ONE = 'one', '★(簡単)'
    growth_environment = models.CharField("成長環境(忙しさ)", choices=Growth_Environment.choices, max_length=10)
    
    # その他
    advantage = models.TextField("強み", max_length=200, default='特になし')
    weaknesses = models.TextField("弱み", max_length=200, default='特になし')
    work_life_balance = models.TextField("ワークライフバランス")
    
    # 応募情報
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company')  # ユーザーと会社の組み合わせは一意

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    preference_level = models.PositiveSmallIntegerField(
        choices=[
            (1, '第一志望'),
            (2, '第二志望'),
            (3, '第三志望'),
            (4, '第四志望'),
            (5, 'その他')
        ],
        default=5  # 例としてデフォルト値を設定
    )

class CompanyNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}: {self.note[:20]}"