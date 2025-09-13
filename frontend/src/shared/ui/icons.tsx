import * as React from "react"
import {
  FaFolder,
  FaPlus,
  FaPenToSquare,
  FaTrash,
  FaBolt,
  FaCrown,
  FaDesktop,
  FaMoon,
  FaUser,
  FaCreditCard,
  FaChartSimple,
  FaRightFromBracket,
  FaShield,
  FaChalkboard,
  FaVideo,
  FaComment,
  FaBuilding,
  FaBox,
  FaHouse,
  FaRocket,
  FaBook,
  FaPalette,
  FaHammer,
  FaRotate,
  FaCartShopping,
  FaGear,
  FaCircleQuestion,
  FaFloppyDisk,
  FaQuoteRight,
  FaPaperclip,
  FaSun,
  FaFolderOpen,
  FaMagnifyingGlass,
  FaBars,
  FaXmark,
  FaImage,
  FaFileArrowUp,
  FaFilePdf,
  FaFileWord,
  FaFileExcel,
  FaFilePowerpoint,
  FaFileCode,
  FaFileVideo,
  FaFileAudio,
  FaFile,
  FaSpinner,
  FaEye,
  FaUsers,
  FaTriangleExclamation,
  FaCheck,
  FaChevronRight,
  FaChevronDown,
  FaCircle,
  FaFilter,
  FaCalendarDays,
  FaTags,
  FaFire,
  FaClock,
  FaBookmark,
  FaShare,
  FaEnvelope,
  FaPaperPlane,
  FaThumbsUp,
  FaThumbsDown,
  FaCircleCheck,
  FaPhone,
  FaHandshake,
  FaBullhorn,
  FaDollarSign,
  FaCalculator,
  FaBell,
  FaWindowMaximize,
  FaArrowUp,
  FaArrowDown,
  FaTelegram,
  FaYoutube,
  FaInstagram,
  FaFacebookF,
  FaLinkedinIn,
  FaTwitter,
  FaVk,
  FaTiktok,
  FaCopyright,
  FaGavel,
  FaCircleQuestion as FaFaqIcon,
  FaBriefcase,
  FaStar,
  FaChevronLeft,
  FaNewspaper,
  FaXTwitter,
  FaReddit,
  FaCookie,
  FaCircleInfo,
  FaComments,
  FaDollarSign as FaMoneyIcon,
  FaRotateLeft,
  FaLocationDot,
  FaHeart,
  // Category icons
  FaMobile,
  FaShirt,
  FaFootball,
  FaCouch,
  FaBookOpen,
  FaCar,
  FaUtensils,
  FaSprayCanSparkles,
  FaGlobe
} from "react-icons/fa6"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

// Posts and content icons
export function PostsIcon({ size = 16, ...props }: IconProps) {
  return <FaNewspaper size={size} {...props} />
}

export function CategoriesIcon({ size = 16, ...props }: IconProps) {
  return <FaFolder size={size} {...props} />
}

// Action icons
export function AddIcon({ size = 16, ...props }: IconProps) {
  return <FaPlus size={size} {...props} />
}

export function EditIcon({ size = 16, ...props }: IconProps) {
  return <FaPenToSquare size={size} {...props} />
}

export function DeleteIcon({ size = 16, ...props }: IconProps) {
  return <FaTrash size={size} {...props} />
}

export function SaveIcon({ size = 16, ...props }: IconProps) {
  return <FaFloppyDisk size={size} {...props} />
}

export function RefreshIcon({ size = 16, ...props }: IconProps) {
  return <FaRotate size={size} {...props} />
}

// Navigation icons
export function HomeIcon({ size = 16, ...props }: IconProps) {
  return <FaHouse size={size} {...props} />
}

export function HubIcon({ size = 16, ...props }: IconProps) {
  return <FaQuoteRight size={size} {...props} />
}

export function SpaceIcon({ size = 16, ...props }: IconProps) {
  return <FaPaperclip size={size} {...props} />
}

export function CatalogIcon({ size = 16, ...props }: IconProps) {
  return <FaFolderOpen size={size} {...props} />
}

export function GlobeIcon({ size = 16, ...props }: IconProps) {
  return <FaGlobe size={size} {...props} />
}

// User and account icons
export function UserIcon({ size = 16, ...props }: IconProps) {
  return <FaUser size={size} {...props} />
}

export function AdminIcon({ size = 16, ...props }: IconProps) {
  return <FaCrown size={size} {...props} />
}

export function LogoutIcon({ size = 16, ...props }: IconProps) {
  return <FaRightFromBracket size={size} {...props} />
}

// UI and system icons
export function SettingsIcon({ size = 16, ...props }: IconProps) {
  return <FaGear size={size} {...props} />
}

export function QuestionIcon({ size = 16, ...props }: IconProps) {
  return <FaCircleQuestion size={size} {...props} />
}

export function DemoIcon({ size = 16, ...props }: IconProps) {
  return <FaBolt size={size} {...props} />
}

// Theme icons
export function SunIcon({ size = 16, ...props }: IconProps) {
  return <FaSun size={size} {...props} />
}

export function MoonIcon({ size = 16, ...props }: IconProps) {
  return <FaMoon size={size} {...props} />
}

export function ComputerIcon({ size = 16, ...props }: IconProps) {
  return <FaDesktop size={size} {...props} />
}

// Business and commerce icons
export function CreditCardIcon({ size = 16, ...props }: IconProps) {
  return <FaCreditCard size={size} {...props} />
}

export function ShoppingIcon({ size = 16, ...props }: IconProps) {
  return <FaCartShopping size={size} {...props} />
}

export function ChartIcon({ size = 16, ...props }: IconProps) {
  return <FaChartSimple size={size} {...props} />
}

export function BuildingIcon({ size = 16, ...props }: IconProps) {
  return <FaBuilding size={size} {...props} />
}

// Content and media icons
export function BookIcon({ size = 16, ...props }: IconProps) {
  return <FaBook size={size} {...props} />
}

export function VideoIcon({ size = 16, ...props }: IconProps) {
  return <FaVideo size={size} {...props} />
}

export function MessageIcon({ size = 16, ...props }: IconProps) {
  return <FaComment size={size} {...props} />
}

export function WhiteboardIcon({ size = 16, ...props }: IconProps) {
  return <FaChalkboard size={size} {...props} />
}

// Tools and utilities icons
export function PaletteIcon({ size = 16, ...props }: IconProps) {
  return <FaPalette size={size} {...props} />
}

export function ConstructionIcon({ size = 16, ...props }: IconProps) {
  return <FaHammer size={size} {...props} />
}

export function BoxIcon({ size = 16, ...props }: IconProps) {
  return <FaBox size={size} {...props} />
}

export function ShieldIcon({ size = 16, ...props }: IconProps) {
  return <FaShield size={size} {...props} />
}

export function RocketIcon({ size = 16, ...props }: IconProps) {
  return <FaRocket size={size} {...props} />
}

// Search and navigation icons
export function SearchIcon({ size = 16, ...props }: IconProps) {
  return <FaMagnifyingGlass size={size} {...props} />
}

export function MenuIcon({ size = 16, ...props }: IconProps) {
  return <FaBars size={size} {...props} />
}

export function CloseIcon({ size = 16, ...props }: IconProps) {
  return <FaXmark size={size} {...props} />
}

export function LoadingIcon({ size = 16, ...props }: IconProps) {
  return <FaSpinner size={size} {...props} />
}

export function EyeIcon({ size = 16, ...props }: IconProps) {
  return <FaEye size={size} {...props} />
}

export function UsersIcon({ size = 16, ...props }: IconProps) {
  return <FaUsers size={size} {...props} />
}

export function AlertIcon({ size = 16, ...props }: IconProps) {
  return <FaTriangleExclamation size={size} {...props} />
}

export function CheckIcon({ size = 16, ...props }: IconProps) {
  return <FaCheck size={size} {...props} />
}

export function ChevronRightIcon({ size = 16, ...props }: IconProps) {
  return <FaChevronRight size={size} {...props} />
}

export function ChevronDownIcon({ size = 16, ...props }: IconProps) {
  return <FaChevronDown size={size} {...props} />
}

export function CircleIcon({ size = 16, ...props }: IconProps) {
  return <FaCircle size={size} {...props} />
}

// Filter and sort icons
export function FilterIcon({ size = 16, ...props }: IconProps) {
  return <FaFilter size={size} {...props} />
}

export function CalendarIcon({ size = 16, ...props }: IconProps) {
  return <FaCalendarDays size={size} {...props} />
}

export function TagIcon({ size = 16, ...props }: IconProps) {
  return <FaTags size={size} {...props} />
}

export function TrendingIcon({ size = 16, ...props }: IconProps) {
  return <FaFire size={size} {...props} />
}

export function ClockIcon({ size = 16, ...props }: IconProps) {
  return <FaClock size={size} {...props} />
}

// Action icons
export function BookmarkIcon({ size = 16, ...props }: IconProps) {
  return <FaBookmark size={size} {...props} />
}

export function ShareIcon({ size = 16, ...props }: IconProps) {
  return <FaShare size={size} {...props} />
}

export function HeartIcon({ size = 16, ...props }: IconProps) {
  return <FaHeart size={size} {...props} />
}

export function LightningIcon({ size = 16, ...props }: IconProps) {
  return <FaBolt size={size} {...props} />
}

// Communication icons
export function MailIcon({ size = 16, ...props }: IconProps) {
  return <FaEnvelope size={size} {...props} />
}

export function SendIcon({ size = 16, ...props }: IconProps) {
  return <FaPaperPlane size={size} {...props} />
}

// Feedback icons
export function ThumbsUpIcon({ size = 16, ...props }: IconProps) {
  return <FaThumbsUp size={size} {...props} />
}

export function ThumbsDownIcon({ size = 16, ...props }: IconProps) {
  return <FaThumbsDown size={size} {...props} />
}

export function CheckCircleIcon({ size = 16, ...props }: IconProps) {
  return <FaCircleCheck size={size} {...props} />
}

// Business icons
export function PhoneIcon({ size = 16, ...props }: IconProps) {
  return <FaPhone size={size} {...props} />
}

export function HandshakeIcon({ size = 16, ...props }: IconProps) {
  return <FaHandshake size={size} {...props} />
}

export function BullhornIcon({ size = 16, ...props }: IconProps) {
  return <FaBullhorn size={size} {...props} />
}

export function DollarIcon({ size = 16, ...props }: IconProps) {
  return <FaDollarSign size={size} {...props} />
}

// Demo-specific icons
export function CalculatorIcon({ size = 16, ...props }: IconProps) {
  return <FaCalculator size={size} {...props} />
}

export function BellIcon({ size = 16, ...props }: IconProps) {
  return <FaBell size={size} {...props} />
}

export function WindowIcon({ size = 16, ...props }: IconProps) {
  return <FaWindowMaximize size={size} {...props} />
}

export function ArrowUpIcon({ size = 16, ...props }: IconProps) {
  return <FaArrowUp size={size} {...props} />
}

export function ArrowDownIcon({ size = 16, ...props }: IconProps) {
  return <FaArrowDown size={size} {...props} />
}

// Additional icons for category management
export function ImageIcon({ size = 16, ...props }: IconProps) {
  return <FaImage size={size} {...props} />
}

export function UploadIcon({ size = 16, ...props }: IconProps) {
  return <FaFileArrowUp size={size} {...props} />
}

// File type icons
export function PdfIcon({ size = 16, ...props }: IconProps) {
  return <FaFilePdf size={size} {...props} />
}

export function WordIcon({ size = 16, ...props }: IconProps) {
  return <FaFileWord size={size} {...props} />
}

export function ExcelIcon({ size = 16, ...props }: IconProps) {
  return <FaFileExcel size={size} {...props} />
}

export function PowerpointIcon({ size = 16, ...props }: IconProps) {
  return <FaFilePowerpoint size={size} {...props} />
}

export function CodeIcon({ size = 16, ...props }: IconProps) {
  return <FaFileCode size={size} {...props} />
}

export function FileVideoIcon({ size = 16, ...props }: IconProps) {
  return <FaFileVideo size={size} {...props} />
}

export function FileAudioIcon({ size = 16, ...props }: IconProps) {
  return <FaFileAudio size={size} {...props} />
}

export function FileIcon({ size = 16, ...props }: IconProps) {
  return <FaFile size={size} {...props} />
}

export function ArchiveIcon({ size = 16, ...props }: IconProps) {
  return <FaBox size={size} {...props} />
}

export function XIcon({ size = 16, ...props }: IconProps) {
  return <FaXmark size={size} {...props} />
}

export function CancelIcon({ size = 16, ...props }: IconProps) {
  return <FaXmark size={size} {...props} />
}

// Social Media Icons
export function TelegramIcon({ size = 16, ...props }: IconProps) {
  return <FaTelegram size={size} {...props} />
}

export function YoutubeIcon({ size = 16, ...props }: IconProps) {
  return <FaYoutube size={size} {...props} />
}

export function InstagramIcon({ size = 16, ...props }: IconProps) {
  return <FaInstagram size={size} {...props} />
}

export function FacebookIcon({ size = 16, ...props }: IconProps) {
  return <FaFacebookF size={size} {...props} />
}

export function LinkedinIcon({ size = 16, ...props }: IconProps) {
  return <FaLinkedinIn size={size} {...props} />
}

export function TwitterIcon({ size = 16, ...props }: IconProps) {
  return <FaTwitter size={size} {...props} />
}

export function TwitterXIcon({ size = 16, ...props }: IconProps) {
  return <FaXTwitter size={size} {...props} />
}

export function VkIcon({ size = 16, ...props }: IconProps) {
  return <FaVk size={size} {...props} />
}

export function TiktokIcon({ size = 16, ...props }: IconProps) {
  return <FaTiktok size={size} {...props} />
}

export function RedditIcon({ size = 16, ...props }: IconProps) {
  return <FaReddit size={size} {...props} />
}

// Footer Related Icons
export function CopyrightIcon({ size = 16, ...props }: IconProps) {
  return <FaCopyright size={size} {...props} />
}

export function LegalIcon({ size = 16, ...props }: IconProps) {
  return <FaGavel size={size} {...props} />
}

export function FaqIcon({ size = 16, ...props }: IconProps) {
  return <FaFaqIcon size={size} {...props} />
}

export function CompanyIcon({ size = 16, ...props }: IconProps) {
  return <FaBriefcase size={size} {...props} />
}

export function StarIcon({ size = 16, ...props }: IconProps) {
  return <FaStar size={size} {...props} />
}

export function ChevronLeftIcon({ size = 16, ...props }: IconProps) {
  return <FaChevronLeft size={size} {...props} />
}

export function ReviewsIcon({ size = 16, ...props }: IconProps) {
  return <FaComment size={size} {...props} />
}

// Additional footer icons
export function CookieIcon({ size = 16, ...props }: IconProps) {
  return <FaCookie size={size} {...props} />
}

export function AboutIcon({ size = 16, ...props }: IconProps) {
  return <FaCircleInfo size={size} {...props} />
}

export function FeedbackIcon({ size = 16, ...props }: IconProps) {
  return <FaComments size={size} {...props} />
}

export function NewsIcon({ size = 16, ...props }: IconProps) {
  return <FaNewspaper size={size} {...props} />
}

export function RefundIcon({ size = 16, ...props }: IconProps) {
  return <FaRotateLeft size={size} {...props} />
}

export function RatesIcon({ size = 16, ...props }: IconProps) {
  return <FaMoneyIcon size={size} {...props} />
}

export function LocationIcon({ size = 16, ...props }: IconProps) {
  return <FaLocationDot size={size} {...props} />
}

// Category icons
export function ClothingIcon({ size = 16, ...props }: IconProps) {
  return <FaShirt size={size} {...props} />
}

export function ElectronicsIcon({ size = 16, ...props }: IconProps) {
  return <FaMobile size={size} {...props} />
}

export function SportsIcon({ size = 16, ...props }: IconProps) {
  return <FaFootball size={size} {...props} />
}

export function HomeGardenIcon({ size = 16, ...props }: IconProps) {
  return <FaCouch size={size} {...props} />
}

export function BooksIcon({ size = 16, ...props }: IconProps) {
  return <FaBookOpen size={size} {...props} />
}

export function AutoMotoIcon({ size = 16, ...props }: IconProps) {
  return <FaCar size={size} {...props} />
}

export function FoodBeverageIcon({ size = 16, ...props }: IconProps) {
  return <FaUtensils size={size} {...props} />
}

export function BeautyHealthIcon({ size = 16, ...props }: IconProps) {
  return <FaSprayCanSparkles size={size} {...props} />
}

export function BagsAccessoriesIcon({ size = 16, ...props }: IconProps) {
  return <FaBox size={size} {...props} />
}

export function HobbiesCreativityIcon({ size = 16, ...props }: IconProps) {
  return <FaPalette size={size} {...props} />
}

// Aliases for consistency with CLAUDE.md examples
export const PlusIcon = AddIcon
export const TrashIcon = DeleteIcon
export const NewspaperIcon = PostsIcon
