import * as React from "react"
import {
  FaFileAlt,
  FaFolder,
  FaPlus,
  FaPencilAlt,
  FaTrash,
  FaBolt,
  FaCrown,
  FaDesktop,
  FaMoon,
  FaUser,
  FaCreditCard,
  FaChartBar,
  FaSignOutAlt,
  FaShieldAlt,
  FaChalkboard,
  FaVideo,
  FaComment,
  FaBuilding,
  FaBox,
  FaHome,
  FaRocket,
  FaBook,
  FaPalette,
  FaHammer,
  FaSync,
  FaShoppingCart,
  FaCog,
  FaQuestionCircle,
  FaSave,
  FaQuoteRight,
  FaPaperclip,
  FaSun,
  FaFolderOpen,
  FaSearch,
  FaBars,
  FaTimes,
  FaSpinner,
  FaEye,
  FaUsers,
  FaExclamationTriangle,
  FaCheck,
  FaChevronRight,
  FaCircle,
  FaFilter,
  FaCalendarAlt,
  FaTags,
  FaFire,
  FaClock,
  FaBookmark,
  FaShare,
  FaEnvelope,
  FaPaperPlane,
  FaThumbsUp,
  FaThumbsDown,
  FaCheckCircle,
  FaPhone,
  FaHandshake,
  FaBullhorn,
  FaDollarSign,
  FaCalculator,
  FaBell,
  FaWindowMaximize
} from "react-icons/fa"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

// Posts and content icons
export function PostsIcon({ size = 16, ...props }: IconProps) {
  return <FaFileAlt size={size} {...props} />
}

export function CategoriesIcon({ size = 16, ...props }: IconProps) {
  return <FaFolder size={size} {...props} />
}

// Action icons
export function AddIcon({ size = 16, ...props }: IconProps) {
  return <FaPlus size={size} {...props} />
}

export function EditIcon({ size = 16, ...props }: IconProps) {
  return <FaPencilAlt size={size} {...props} />
}

export function DeleteIcon({ size = 16, ...props }: IconProps) {
  return <FaTrash size={size} {...props} />
}

export function SaveIcon({ size = 16, ...props }: IconProps) {
  return <FaSave size={size} {...props} />
}

export function RefreshIcon({ size = 16, ...props }: IconProps) {
  return <FaSync size={size} {...props} />
}

// Navigation icons
export function HomeIcon({ size = 16, ...props }: IconProps) {
  return <FaHome size={size} {...props} />
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

// User and account icons
export function UserIcon({ size = 16, ...props }: IconProps) {
  return <FaUser size={size} {...props} />
}

export function AdminIcon({ size = 16, ...props }: IconProps) {
  return <FaCrown size={size} {...props} />
}

export function LogoutIcon({ size = 16, ...props }: IconProps) {
  return <FaSignOutAlt size={size} {...props} />
}

// UI and system icons
export function SettingsIcon({ size = 16, ...props }: IconProps) {
  return <FaCog size={size} {...props} />
}

export function QuestionIcon({ size = 16, ...props }: IconProps) {
  return <FaQuestionCircle size={size} {...props} />
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
  return <FaShoppingCart size={size} {...props} />
}

export function ChartIcon({ size = 16, ...props }: IconProps) {
  return <FaChartBar size={size} {...props} />
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
  return <FaShieldAlt size={size} {...props} />
}

export function RocketIcon({ size = 16, ...props }: IconProps) {
  return <FaRocket size={size} {...props} />
}

// Search and navigation icons
export function SearchIcon({ size = 16, ...props }: IconProps) {
  return <FaSearch size={size} {...props} />
}

export function MenuIcon({ size = 16, ...props }: IconProps) {
  return <FaBars size={size} {...props} />
}

export function CloseIcon({ size = 16, ...props }: IconProps) {
  return <FaTimes size={size} {...props} />
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
  return <FaExclamationTriangle size={size} {...props} />
}

export function CheckIcon({ size = 16, ...props }: IconProps) {
  return <FaCheck size={size} {...props} />
}

export function ChevronRightIcon({ size = 16, ...props }: IconProps) {
  return <FaChevronRight size={size} {...props} />
}

export function CircleIcon({ size = 16, ...props }: IconProps) {
  return <FaCircle size={size} {...props} />
}

// Filter and sort icons
export function FilterIcon({ size = 16, ...props }: IconProps) {
  return <FaFilter size={size} {...props} />
}

export function CalendarIcon({ size = 16, ...props }: IconProps) {
  return <FaCalendarAlt size={size} {...props} />
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
  return <FaCheckCircle size={size} {...props} />
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